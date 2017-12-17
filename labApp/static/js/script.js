console.log('get into scripts.js');

$(document).ready(function(){
    console.log('Document is ready');

 /*   if(document.URL.match('hw/hotels')){
        load_last_bookings();
        $("#id_start_date_month").change(calc_price);
        $("#id_start_date_day").change(calc_price);
        $("#id_start_date_year").change(calc_price);
        $("#id_end_date_month").change(calc_price);
        $("#id_end_date_day").change(calc_price);
        $("#id_end_date_year").change(calc_price);
    }
*/
    //при нажатию на любую кнопку, имеющую класс .btn_modal_order (открытие модального окна "заказать")
    $(".btn_modal_order").click(function() {
        console.log('жмяк btn_modal_order');
        //открыть модальное окно с id="modalOrder"
        $("#modalOrdering").modal('show');
        $("#id_user").val($('#customer_name').text());
        $("#id_prodact").val($('#prodact_name').text());
        $("#id_date").val(new Date()); /////////------!!!
    });

    //нажатие на кнопку "заказать"
    $('#btn_order').click(function() {
        console.log('жмяк btn_order');
        //if(isNaN(Number($('#id_number').val())) || (Number($('#id_number').val()))<=0){ //Если оличество таваров - не число или меньше нуля => ошибка
            //return;
        //}

        var csrf_value = document.getElementsByName("csrfmiddlewaretoken")[0].getAttribute("value");
        console.log(csrf_value)
        $.ajax({
            type: "POST",
            url: '/hw/ajax/order/', //!!!
            data: {
                'prodact_name': $("#id_prodact").val(),
                'user_email': $("#customer_email").text(),
                'number': $("#id_number").val(),
                'date': $("#id_date").val(),
                csrfmiddlewaretoken: csrf_value,
            },
            dataType: 'html',
            success: function(data){
                $('#success_order').text('Бронирование успешно выполнено');
                $('#success_order').show();
                $('#btn_order').hide();

                console.log('success');
                console.log(data);
            },
            failure: function(data){
                console.log('failure');
                console.log(data);
            },
            /*complete: function(){
                load_last_bookings();
            },*/
        })
    })
});