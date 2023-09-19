function Aprove_pymt(args,url){
   $.ajax({
        type  : "GET",
        url   : url,
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#event-order").html(response['data']);  
        },
        error :function(error){
            alert('error');
        }
    })

   
}