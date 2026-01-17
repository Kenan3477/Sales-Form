// Optional: configure or set up a testing framework before each test.
// If you delete this file, remove `setupFilesAfterEnv` from `jest.config.js`

// Mock implementations that are needed across tests
global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

// Mock FormData for Node.js environment
if (!global.FormData) {
  global.FormData = require('form-data')
}

// Mock File API for Node.js environment
if (!global.File) {
  global.File = class File {
    constructor(bits, name, options = {}) {
      this.bits = bits
      this.name = name
      this.type = options.type || ''
      this.size = bits.reduce((size, bit) => size + bit.length, 0)
    }
  }
}

// Mock Blob API for Node.js environment
if (!global.Blob) {
  global.Blob = class Blob {
    constructor(parts = [], options = {}) {
      this.parts = parts
      this.type = options.type || ''
      this.size = parts.reduce((size, part) => size + (part.length || 0), 0)
    }
  }
}