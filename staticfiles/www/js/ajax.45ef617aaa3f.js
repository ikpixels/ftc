
$(document).ready(function(){

    $('#option_cart_form').on('submit', function(event){
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
            location.href = '/cart/cart_view/';
            
            
        },
        error :function(error){
            main_error();
        }
    })
    
    
  });

})

function delete_shop_item(args){
  
     $.ajax({
        type  : "GET",
        url   : args,
        data  : {'data':"delet", 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#main_shop_item").html(response['data'])
            $('#removed_suc').css('display','block');
         
        },
        error :function(error){
            main_error();
        }
    })
}

function delete_item(item){
    url = item

    $.ajax({
        type  : "GET",
        url   : url,
        data  : {'data':"delete", 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            location.href = '/cart/cart_view/';
            
            
        },
        error :function(error){
            main_error();
        }
    })
}


//____________________________________________________________
function shiping(args){

    if($(args).is(":checked")){
         $('#billing_info').css('display','none');//when checked
         $('#shipping_info').css('display','block')
         $('#shipping_btn').css('display','none');
         
  
    }else{
        $('#billing_info').css('display','block');//when not checked
        $('#shipping_info').css('display','none')
        $('#shipping_btn').css('display','block');
     
  }
}
//_____________________________________________________________          
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
            main_error();
        }
    })
    
    
  });

})


function item_sold(args){


    $.ajax({
        type  : "GET",
        url   : args,
   
        success : function(response){
            $("#item_sold").html(response['data'])
            
            
        },
        error :function(error){
            main_error();
        }
    })
}

function free_plan(args){


    $.ajax({
        type  : "GET",
        url   : args,
   
        success : function(response){
            location.href = "/vendor/payment_feedback/"
                
        },
        error :function(error){
            main_error();
        }
    })
}

$(document).ready(function(){

    $('#add_category').on('submit', function(event){
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
            $("#inner_category").html(response['data'])
            
            
        },
        error :function(error){
            main_error();
        }
    })
    
    
  });

})
function top_seller(args){
     $.ajax({
        type  : "GET",
        url   : '/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $(".main_item3").html(response['data'])
         
        },
        error :function(error){
           main_error();
        }
    }) 
    $('#top_seller').css('color','red'); 
    $('#Popular').css('color','orange');
    $('#top_rated').css('color','orange');
    
}
function Popular(args){
    $.ajax({
        type  : "GET",
        url   : '/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $(".main_item3").html(response['data'])
         
        },
        error :function(error){
            $('#main_alert').css('display','block');
            $('#inner_main_alert_text').html("Something is wrong");
      
        }
    })
    $('#Popular').css('color','red'); 
    $('#top_seller').css('color','orange'); 
    $('#top_rated').css('color','orange');
}
function top_rated(args){
    $.ajax({
        type  : "GET",
        url   : '/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $(".main_item3").html(response['data'])
         
        },
        error :function(error){
            main_error();
        }
    })
    $('#top_rated').css('color','red');
    $('#Popular').css('color','orange'); 
    $('#top_seller').css('color','orange');
}
$(document).ready(function(){

var num = $("#mywap").attr('accesskey');
    $('#mywap').floatingWhatsApp({
    phone:num,
    popupMessage: 'Hello, Lets chat',
    showPopup: true,
    //showOnIE: false,
    //headerTitle: 'Welcome!',
    //headerColor: 'crimson',
    //backgroundColor: 'crimson',
    });
})
$(document).ready(function(){

var num = $("#additem_wap").attr('accesskey');
    $('#additem_wap').floatingWhatsApp({
    phone:num,
    popupMessage: 'Hello, Send your item info here',
    showPopup: true,
    //showOnIE: false,
    //headerTitle: 'Welcome!',
    //headerColor: 'crimson',
    //backgroundColor: 'crimson',
    });
})
function cart_detail(args){
    $.ajax({
        type  : "GET",
        url   : '/account/cart_detail/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $(".dashboard_detail_area").html(response['data'])
         
        },
        error :function(error){
           main_error();
        }
    })
}
function ivoice(){
    
    $.ajax({
        type  : "GET",
        url   : '/cart/paypal_thax/',
        data  : {'data':'delete', 'csrfmiddlewaretoken': '{{ csrf_token }}'},

        success : function(response){
            $(".dashboard_detail_area").html(response['data'])
         
        },
        error :function(error){
           main_error();
        }
    })
}
function delivered(args){
    $.ajax({
        type  : "GET",
        url   : '/cart/delivered/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            location.href = '/account/dashboard/'
         
        },
        error :function(error){
            main_error();
        }
    })
}
//payment verification
function verify(args){
    $.ajax({
        type  : "GET",
        url   : '/cart/Payment_verification/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#verification_table").html(response['data'])
         
        },
        error :function(error){
            main_error();
        }
    })
}



function edit_main_shop_item(args){
    location.href = args;
}


function remove_category(args){

    $.ajax({
        type  : "GET",
        url   : '/products/remove_category/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){;
            $("#inner_category").html(response['data'])  
        },
        error :function(error){
           main_error();
        }
    })
}
function plan_activate(args){
    
    $.ajax({
        type  : "GET",
        url   : '/vendor/bill_verification/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){;
            $("#bill_verification").html(response['data'])  
        },
        error :function(error){
            main_error();
        }
    })
}
$(document).ready(function(){

    $('#Comment_Form').on('submit', function(event){
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
            $("#Comment_content").html(response['data']) 
            //location.href = '/cart/cart_view/';
            
            
        },
        error :function(error){
            main_error();
        }
    })
    
    
  });

})
function agent_detail(args){
    css_id = '#agent' + args;
    $(css_id).toggle(1000);  
}
function agent_detail_hide(args){
    css_id = '#agent' + args;
    $(css_id).toggle(1000);  
}
function received_from_vendor(args){
     $.ajax({
        type  : "GET",
        url   : '/account/dashboard/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){;
            $("#item_received").html(response['data'])  
        },
        error :function(error){
            main_error();
        }
    })
}
function deal_activate(args){
    
    $.ajax({
        type  : "GET",
        url   : '/vendor/deal_payment_verification/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#bill_verification").html(response['data']); 
        },
        error :function(error){
            main_error();
        }
    })

}

function download_btn(url,id){
    $('.btn_download').hide();
    
    $.ajax({
        type  : "GET",
        url   : url,
        data  : {'data':id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $('.btn_download2').show();
        },
        error :function(error){
            main_error();
        }
    })

}

function download_payment(args){
    $('#music_download_html').toggle();
}

function video_btn(args){
    $('#music_video_html').slideToggle(1000);
}




function Aprove_music(args){

  $.ajax({
        type  : "GET",
        url   : '/Evet/main_music/',
        data  : {'data':args,'data2':'approve', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#ik_music_manager_area").html(response['data']);
        },
        error :function(error){
            main_error();
        }
    })
}


function disapprove_music(args){

  $.ajax({
        type  : "GET",
        url   : '/music/main_music/',
        data  : {'data':args, 'data2':'disapprove', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#ik_music_manager_area").html(response['data']);
        },
        error :function(error){
            main_error();
        }
    })
}
function delete_music(args){
   $.ajax({
        type  : "GET",
        url   : '/music/user_music_list/',
        data  : {'data':args, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            $("#ik_music_manager_area").html(response['data']);
        },
        error :function(error){
            main_error();
        }
    })
}
$(document).ready(function(){

    $('#place_order_form_nt').on('submit', function(event){
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
            $("#place_order_feedback_area").html(response['data']);
            
            
        },
        error :function(error){
            main_error();
        }
    })
    
    
  });

})
//----------------------------------------------------------------
