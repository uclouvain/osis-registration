const showSpinnerDelay = 800; //ms
const spinnerFadeDuration = 200; //ms

let downloadInterval;
let saveStateInterval;

let loadingCompleted = false;
let linkButtonNoSpinnerClicked = false;
let triggerHtmxRequest = false;

//TODO : remove this after all submodules have removed no_spinner class
function bindNoSpinner(elem){
    linkButtonNoSpinnerClicked = elem ? elem.hasClass("no_spinner") : false;
}

function showOverlaySpinner(rotation=0) {
    const overlay  = $('#overlay');

    if(!loadingCompleted && !triggerHtmxRequest) {
        overlay.fadeTo(spinnerFadeDuration, 1);
        saveSpinnerState();
    }
}

function closeOverlaySpinner(){
    const loaderToHide = $('#overlay');
    loaderToHide.fadeTo(spinnerFadeDuration, 0, () => loaderToHide.hide());
    clearInterval(saveStateInterval);

    // cancel spinner state for future pages
    localStorage.setItem('spinner', JSON.stringify({"state": false}));
}

//handle spinner for download file
function isDownloadCompleted(){
    if(document.cookie.includes('download')){
        loadingCompleted = true;
        closeOverlaySpinner();
        // delete cookie setting an expired date
        document.cookie = "download=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        if(downloadInterval) {
            clearInterval(downloadInterval)
        }
    }
}

function saveSpinnerState() {
    saveStateInterval = setInterval(() => {
        const rotation = getSpinnerRotation();
        localStorage.setItem('spinner', JSON.stringify({"state": true, "rotation": rotation}));
    }, 100);
}

function getSpinnerRotation() {
    let transformMatrix;
    ['-webkit-', '-moz-', '-ms', '-o-', ''].forEach((prefix) => {
        transformMatrix = transformMatrix || $('#loader').css(`${prefix}transform`)
    })
    if(transformMatrix !== 'none') {
         const values = transformMatrix.split('(')[1].split(')')[0].split(',');
         return Math.round(Math.atan2(values[1], values[0]) * (180/Math.PI));
    }
    return 0;
}

window.addEventListener("pageshow", function() {
    $('.download').click(() => {
        downloadInterval = setInterval(isDownloadCompleted, showSpinnerDelay-100); //prevent spinner before its delay
    });

    //TODO : remove this after all submodules have removed no_spinner class
    //bind no spinner for backward compatibility
    $('a, button').on('click submit', function (e) {
        bindNoSpinner($(this));
    });
    ["formAjaxSubmit:onSubmit", "prepareXls:onClick"].forEach( evt =>
        document.addEventListener(evt, function (e) {
            bindNoSpinner(e.detail);
        })
    );

    loadingCompleted = true;
    closeOverlaySpinner();
});

window.addEventListener("htmx:beforeSend", function() {
    triggerHtmxRequest = true;
});

$(document).on('keyup', function (e) {
    if ( e.key === 'Escape' ) { // ESC
        closeOverlaySpinner();
    }
});

window.addEventListener('beforeunload', function (e) {
    loadingCompleted = false;
    if (!linkButtonNoSpinnerClicked) {
        setTimeout(showOverlaySpinner, showSpinnerDelay);
    }
});


$(document).ajaxStart(function(){
    // prevent ajax to trigger spinner when dom is not ready yet
    loadingCompleted = false;
    setTimeout(() => showOverlaySpinner(), showSpinnerDelay);
}).ajaxStop(function(){
    loadingCompleted = true;
    closeOverlaySpinner();
});
