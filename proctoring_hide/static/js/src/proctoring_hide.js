function ProctoringHideXBlock(runtime, element, settings) {
    $(function($) {
        console.log(window.location);
        console.log(window.parent.location)
        console.log(window.top);
        console.log(window.self);
       
        function inIframe () {
            try {
                return window.self !== window.top;
            } catch (e) {
                console.log(e);
                return true;
            }
        }
        if (inIframe()){
            if (window.location.ancestorOrigins[0] == 'https://uchile.proctoring.app'){
                $('#seq_content').show();
            }
            else{
                $('#seq_content').hide();
                alert("Cotenido visible solamente por Proctoring");
            }
        }
        else{
            $('#seq_content').hide();
            alert("Cotenido visible solamente por Proctoring");
        }
    });
}