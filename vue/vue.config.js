const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
    ? '/ebs_t06/' // Set this to the name of your repository on GitHub.
    : '/'
});
