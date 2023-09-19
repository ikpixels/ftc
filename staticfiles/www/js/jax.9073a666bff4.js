function Aprove_pymt(args,url){
   $.ajax({
        type  : "GET",
        url   : url,
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#event-order").html(response['data']);  
        },
        error :function(error){
            alert('Something went wrong');
        }
    })   
}
function add_video_view(args){
     $.ajax({
        type  : "GET",
        url   : '/podcasts/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $('.open-video').css('color','red');
        },
        error :function(error){
            alert('Something went wrong');   
        }
    })
}
function streamingCount(args){
        $.ajax({
        type  : "GET",
        url   : '/Artists/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success : function(response){
            console.clear();
            console.log('added');
        },
        error :function(error){
            alert('Something went wrong');
        }
    })}



