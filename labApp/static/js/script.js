console.log('script.js');

//сумма заказа
function sum_order_price(){
    console.log('sum order price');
    //console.log(document.getElementById("price").innerHTML);
    console.log(Number($("#id_number").text()));
    console.log("цена",$("#price").text())
    console.log($('#price').val().replace(',', '.'))
    console.log("цена",parseFloat($("#price").text().replace(',', '.')))
    price = document.getElementById("price").innerHTML;

    ordprice = parseFloat($("#price").text().replace(',', '.')) * Number($("#id_number").val());
    console.log(ordprice);
    $("#id_order_price").val(ordprice);
}

//вывести  последние заказы данного товара
function load_last_order(){
    console.log('loading last_order');
    console.log($("#prod_id").text())
    $.ajax({
            type: "GET",
            url: '/ajax/last_order/',
            data: {
                'prodact_name': $("#prodact_name").text(),
                'prodact_id': $("#prod_id").text(),
                'username': $("#customer_username").text(),
            },
            dataType: 'html',
            success: function(data){
                if(data == '-'){
                    return;
                }
                $('#last_order_header').show();
                $('#last_order').html(data);

                console.log('success');
                console.log(data);
            },
            failure: function(data){
                console.log('failure');
                console.log(data);
            }
        })
}

$(document).ready(function(){

    console.log('document is ready');

    if(document.URL.match('prodact/')){
        $("#id_number").change(sum_order_price);
        load_last_order();
    }

    //при нажатию на любую кнопку, имеющую класс .btn_modal_order (открытие модального окна "заказать")
    $(".btn_modal_order").click(function() {
        console.log(' btn_modal_order');

        //открыть модальное окно с id="modalOrder"
        $("#modalOrder").modal('show');
        $("#id_user").val($('#customer_name').text());
        $("#id_prodact").val($('#prodact_name').text());


        $('#success_order').hide();
        $('#btn_order').show();
        var num = 1;
        var now = new Date();
        $("#id_order_date").val(now.toLocaleString());
        $("#id_number").val(num);
        sum_order_price();

    });

    //нажатие на кнопку "заказать"
    $('#btn_order').click(function() {
        console.log(' btn_order');
        if(isNaN(Number($('#id_number').val())) || (Number($('#id_number').val())) <= 0){ //Если оличество таваров - не число или меньше нуля => ошибка
            alert('Ошибка! Количество должно быть больше нуля.');
            return;
        }
        console.log($("#prod_id").text())

        var csrf_value = document.getElementsByName("csrfmiddlewaretoken")[0].getAttribute("value");
        console.log(csrf_value);
        $.ajax({
            type: "POST",
            url: '/ajax/order/',
            data: {
                'prodact_name': $("#id_prodact").val(),
                'prodact_id': $("#prod_id").text(),
                'username': $("#customer_username").text(),
                'number': $("#id_number").val(),
                'order_price': $("#id_order_price").val(),
                csrfmiddlewaretoken: csrf_value,
            },
            dataType: 'html',
            success: function(data){
                $('#success_order').text('Заказ выполнен.');
                $('#success_order').show();
                $('#btn_order').hide();
                /*$('#btn_close').click(function () {
                    location.reload();
                })
                $('.close').click(function () {
                    location.reload();
                })*/
                console.log('success');
                console.log(data);
            },
            failure: function(data){
                console.log('failure');
                console.log(data);
            },
            complete: function(){
                load_last_order();
            },
        })
        console.log('ajax finish')
    })

});

//валидация на стороне js
var descriptionArea = document.getElementById('descriptionArea');
var descriptionTip = document.createElement('div');
descriptionTip.className = 'description-tip';
descriptionTip.innerText = 'Слишком короткое описание.';

var showingDescriptionTip = false;

//onfocus
function productDescriptionValidate(event) {
    var target = event.target;
    var coords = target.getBoundingClientRect();

    var left = coords.left + (target.offsetWidth - descriptionTip.offsetWidth) / 2;
    if (left < 0) left = 0; // не вылезать за левую границу окна

    var top = coords.top - descriptionTip.offsetHeight - 5;
    if (top < 0) { // не вылезать за верхнюю границу окна
        top = coords.top + target.offsetHeight + 5;
    }

    descriptionTip.style.left = left + 'px';
    descriptionTip.style.top = top + 'px';


    if (descriptionArea.value.length < 15 && (showingDescriptionTip === false)) {
        document.body.appendChild(descriptionTip);
        showingDescriptionTip = true;
    } else if (descriptionArea.value.length >= 15) {
        descriptionTip.remove();
        showingDescriptionTip = false;
    }
}


//onclick
function validateDescriptionAfterSubmit(event) {

    if (descriptionArea.value.length < 15 && descriptionArea.value.length > 0
        && (showingDescriptionTip === false)) {
        event.preventDefault();
        document.body.appendChild(descriptionTip);
        showingDescriptionTip = true;
    } else if (showingDescriptionTip === true) {
        event.preventDefault();
    }
}
//onblur
function removeDescriptionTipOnBlur() {
    if (showingDescriptionTip) {
        descriptionTip.remove();
        showingDescriptionTip = false;
    }
}

//карусель
$('.carousel').carousel({
    interval: 4000 //changes the speed
})