const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

export default {
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5858'
    }
  }
}
