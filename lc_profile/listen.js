#!/usr/bin/env node

const Promise = require('bluebird')
const { Realtime } = require('leancloud-realtime')

const main = Promise.coroutine(function* () {
  const conn = new Realtime({ appId: process.env.LC_APP_ID })
  const client = yield conn.createIMClient('lc-profile-listener')

  client.on('message', (msg) => {
    const sendAt  = new Date(msg.content.send_at * 1000)
    const remoteReceivedAt = new Date(msg.timestamp)
    const localReceivedAt = new Date()

    const dtRemote = (remoteReceivedAt - sendAt) / 1000
    const dtLocal = (localReceivedAt - remoteReceivedAt) / 1000
    const dtTotal = (localReceivedAt - sendAt) / 1000

    console.log(`Local->Remote:${dtRemote}s; Remote->Local:${dtLocal}s; Total:${dtTotal}s`)
  })
})

main().catch(console.error.bind(console))
