import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';
import path from 'path'
import Vue from '@vitejs/plugin-vue'
const pathSrc = path.resolve(__dirname, 'src')


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    AutoImport({
      imports:['vue'],
      resolvers:[ElementPlusResolver()],
      eslintrc:{enabled:true},
    }),
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver(),IconsResolver({
        prefix: 'Icon',
      }),],
      dts: path.resolve(pathSrc, 'auto-imports.d.ts'),
    }),
    Components({
      dirs: ['src/components/'],
      extensions: ['vue', 'md'],
      resolvers: [IconsResolver({enabledCollections: ['ep'],}),ElementPlusResolver(), AntDesignVueResolver()],
        dts: path.resolve(pathSrc, 'components.d.ts'),
    }),
    Icons({
      compiler: 'vue3',
      autoInstall: true,
    }),
    
  ],
  resolve: {
    alias: {
      '@': pathSrc,
    },
  }
})
