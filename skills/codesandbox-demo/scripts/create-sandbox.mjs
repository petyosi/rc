#!/usr/bin/env node

import { readdir, readFile, stat } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'

const DEFINE_API = 'https://codesandbox.io/api/v1/sandboxes/define?json=1'
const MAX_PAYLOAD_BYTES = 5 * 1024 * 1024
const ignoredDirectories = new Set(['.git', 'build', 'coverage', 'dist', 'node_modules'])
const ignoredFiles = new Set(['.DS_Store'])

function usage() {
  console.error('Usage: node create-sandbox.mjs <project-directory> [open-file]')
  process.exit(2)
}

function isSecretFile(relativePath) {
  const basename = path.posix.basename(relativePath).toLowerCase()
  return (
    basename === '.env' ||
    basename.startsWith('.env.') ||
    basename === 'credentials.json' ||
    basename === 'id_rsa' ||
    basename === 'id_ed25519' ||
    basename.endsWith('.key') ||
    basename.endsWith('.pem')
  )
}

async function collectFiles(root, current = '') {
  const entries = await readdir(path.join(root, current), { withFileTypes: true })
  const files = {}

  for (const entry of entries) {
    const relativePath = path.posix.join(current, entry.name)

    if (entry.isSymbolicLink()) {
      throw new Error(`Refusing to submit symlink: ${relativePath}`)
    }
    if (entry.isDirectory()) {
      if (!ignoredDirectories.has(entry.name)) {
        Object.assign(files, await collectFiles(root, relativePath))
      }
      continue
    }
    if (!entry.isFile() || ignoredFiles.has(entry.name)) continue
    if (isSecretFile(relativePath)) {
      throw new Error(`Refusing to submit possible secret file: ${relativePath}`)
    }

    const contents = await readFile(path.join(root, relativePath))
    if (contents.includes(0)) {
      throw new Error(`CodeSandbox Define API accepts text files only: ${relativePath}`)
    }
    files[relativePath] = { content: contents.toString('utf8') }
  }

  return files
}

const [, , projectDirectory, requestedOpenFile] = process.argv
if (!projectDirectory) usage()

const root = path.resolve(projectDirectory)
if (!(await stat(root)).isDirectory()) {
  throw new Error(`Not a directory: ${root}`)
}

const files = await collectFiles(root)
if (Object.keys(files).length === 0) {
  throw new Error(`No files found in ${root}`)
}

const body = JSON.stringify({ files })
if (Buffer.byteLength(body) > MAX_PAYLOAD_BYTES) {
  throw new Error('Sandbox payload exceeds the 5 MiB safety limit')
}

const response = await fetch(DEFINE_API, {
  method: 'POST',
  headers: {
    accept: 'application/json',
    'content-type': 'application/json',
  },
  body,
})

if (!response.ok) {
  throw new Error(`CodeSandbox returned ${response.status}: ${await response.text()}`)
}

const result = await response.json()
if (!result.sandbox_id) {
  throw new Error(`CodeSandbox response has no sandbox_id: ${JSON.stringify(result)}`)
}

const openFile = requestedOpenFile?.replace(/^\//, '')
const fileQuery = openFile ? `?file=${encodeURIComponent(`/${openFile}`)}` : ''

console.log(`Sandbox ID: ${result.sandbox_id}`)
console.log(`Editor: https://codesandbox.io/s/${result.sandbox_id}${fileQuery}`)
console.log(`Preview: https://${result.sandbox_id}.csb.app/`)
