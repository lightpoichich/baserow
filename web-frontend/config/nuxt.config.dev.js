import _ from 'lodash'
import StyleLintPlugin from 'stylelint-webpack-plugin'

import base from './nuxt.config.base.js'

export default _.assign(base(), {
  build: {
    extend(config, ctx) {
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
        })
      }
    },

    plugins: [
      new StyleLintPlugin({
        syntax: 'scss',
      }),
    ],
  },
})
