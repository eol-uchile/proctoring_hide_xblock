function ProctoringHideXBlock(runtime, element, settings) {
    $(function($) {
        function inIframe () {
            try {
                return window.self !== window.top;
            } catch (e) {
                console.log(e);
                return true;
            }
        }
        if (!settings.is_staff){
            if (inIframe()){
                if (window.location.ancestorOrigins[0] == settings.proctor_url ){
                    $('#seq_content').show();
                }
                else{
                    $('#seq_content').hide();
                    alert("Contenido visible solamente por Proctoring");
                }
            }
            else{
                $('#seq_content').hide();
                alert("Contenido visible solamente por Proctoring");
            }
        }
    });
}