$(document).ready(function(){

    $('#contact_form').on('submit', function(event){
    event.preventDefault();
    var this_form = $(this);
    var url = this_form.attr('action');
    var data = this_form.serialize();
    $.ajax({
        type  : "GET",
        url   : url,
        data  : data,
        

        success : function(response){
            this_form[0].reset();
            $('#success_c').css('display','block');
            
            
        },
        error :function(error){
            alert('something is wrong!!');
        }
    })
    
    
  });

//-------------------------------Signup-------------------------------------------------------
$('#signupForm').on('submit', function(event){
    event.preventDefault();
    var this_form = $(this);
    var url = '/accountsignup/';
    var data = this_form.serialize();

    if ($('input[name=remember]').is(':checked')){
        $.ajax({
        type  : "POST",
        url   : url,
        data  : data,
        

        success : function(response){
            this_form[0].reset();
            location.href = '/accountprofile/';  
        },
        error :function(error){
            alert('something is wrong!!');
        }
    })
    }else{
        $('#privency').css('display','block');
            
    }

  });
//----------------------------------------------------------------------------------------------

})

$(document).ready(function(){

    $('#comments__form').on('submit', function(event){
    event.preventDefault();
    var this_form = $(this);
    var url = this_form.attr('action');
    var data = this_form.serialize();
    $.ajax({
        type  : "GET",
        url   : url,
        data  : data,
        

        success : function(response){
            this_form[0].reset();
            $(".msg-Comments").html(response['data']);  
        },
        error :function(error){
            alert('something is wrong!!');
        }
    })
    
    
  });

})



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

$('#download').click(function(e) {
    e.preventDefault();  //stop the browser from following
    var a = $(this);
    var link = a.attr('href');
    var url = a.attr('target');
    var id = a.attr('accesskey');
   
    $.ajax({
        type  : "GET",
        url   : url,
        data  : {'song_id':id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success : function(response){
            window.location.href = link;
            
        },
        error :function(error){
            alert('Something went wrong');
        }
    })
});