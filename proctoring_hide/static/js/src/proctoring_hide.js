function ProctoringHideXBlock(runtime, element, settings) {
    $(function($) {
        console.log(window.location);
        console.log(window.top);
        console.log(window.self);
        $('#seq_content').hide()
        function inIframe () {
            try {
                return window.self !== window.top;
            } catch (e) {
                console.log(e);
                return true;
            }
        }
        if (inIframe ()){
            console.log('inIframe');
        }
        else{
            console.log('Not inIframe');
        }
    });
}