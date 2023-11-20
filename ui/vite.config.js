import { basename } from 'path'
import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [svelte()],
    base: './',
    publicDir: false,
    build: {
        minify: false,
        outDir: 'build',
        // build the js in library mode, the html files are served by django
        lib: {
            entry: ["./src/main.js"],
            formats: ['es'],
            name: 'App',
            fileName: (fmt, ent) => basename(ent) + '.js',
        },
        watch: true,
        sourcemap: false,
    },
    optimizeDeps: {
        // needed for tailwindcss to parse
        include: ['templates/**'],
    },
});