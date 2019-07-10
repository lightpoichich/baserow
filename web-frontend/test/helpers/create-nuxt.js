import { Builder, Nuxt } from 'nuxt'

import config from '@/config/nuxt.config.test'

export default async function createNuxt(buildAndListen = false) {
  const nuxt = new Nuxt(config)
  await nuxt.ready()
  if (buildAndListen) {
    await new Builder(nuxt).build()
    await nuxt.server.listen(3001, 'localhost')
  }
  return nuxt
}
