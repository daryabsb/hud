import PhotoSwipeLightbox from "/static/app/plugins/photoswipe/dist/photoswipe-lightbox.esm.js";
const lightbox = new PhotoSwipeLightbox({
    gallery: '.gallery-image-list',
    children: 'a',
    pswpModule: () => import("/static/app/plugins/photoswipe/dist/photoswipe.esm.js")
}); lightbox.init();