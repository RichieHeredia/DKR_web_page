(function($) {

    $( "#birth_date" ).datepicker({
        dateFormat: "mm - dd - yy",
        showOn: "both",
        buttonText : '<i class="zmdi zmdi-calendar-alt"></i>',
    });

    $('.add-info-link ').on('click', function() {
        $('.add_info').toggle( "slow" );
    });

    $('#country').parent().append('<ul class="list-item" id="newcountry" name="country"></ul>');
    $('#country option').each(function(){
        $('#newcountry').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#country').remove();
    $('#newcountry').attr('id', 'country');
    $('#country li').first().addClass('init');
    $("#country").on("click", ".init", function() {
        $(this).closest("#country").children('li:not(.init)').toggle();
    });

    $('#city').parent().append('<ul class="list-item" id="newcity" name="city"></ul>');
    $('#city option').each(function(){
        $('#newcity').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#city').remove();
    $('#newcity').attr('id', 'city');
    $('#city li').first().addClass('init');
    $("#city").on("click", ".init", function() {
        $(this).closest("#city").children('li:not(.init)').toggle();
    });

    $('#place').parent().append('<ul class="list-item" id="newplace" name="place"></ul>');
    $('#place option').each(function(){
        $('#newplace').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#place').remove();
    $('#newplace').attr('id', 'place');
    $('#place li').first().addClass('init');
    $("#place").on("click", ".init", function() {
        $(this).closest("#place").children('li:not(.init)').toggle();
    });

    $('#bank').parent().append('<ul class="list-item" id="newbank" name="bank"></ul>');
    $('#bank option').each(function(){
        $('#newbank').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#bank').remove();
    $('#newbank').attr('id', 'bank');
    $('#bank li').first().addClass('init');
    $("#bank").on("click", ".init", function() {
        $(this).closest("#bank").children('li:not(.init)').toggle();
    });

    $('#activity').parent().append('<ul class="list-item" id="newactivity" name="activity"></ul>');
    $('#activity option').each(function(){
        $('#newactivity').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#activity').remove();
    $('#newactivity').attr('id', 'activity');
    $('#activity li').first().addClass('init');
    $("#activity").on("click", ".init", function() {
        $(this).closest("#activity").children('li:not(.init)').toggle();
    });

    $('#member').parent().append('<ul class="list-item" id="newmember" name="member"></ul>');
    $('#member option').each(function(){
        $('#newmember').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#member').remove();
    $('#newmember').attr('id', 'member');
    $('#member li').first().addClass('init');
    $("#member").on("click", ".init", function() {
        $(this).closest("#member").children('li:not(.init)').toggle();
    });

    var allOptions = $("#country").children('li:not(.init)');
    $("#country").on("click", "li:not(.init)", function() {
        allOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#country").children('.init').html($(this).html());
        allOptions.toggle('slow');
    });

    var FoodOptions = $("#city").children('li:not(.init)');
    $("#city").on("click", "li:not(.init)", function() {
        FoodOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#city").children('.init').html($(this).html());
        FoodOptions.toggle('slow');
    });

    var placeOptions = $("#place").children('li:not(.init)');
    $("#place").on("click", "li:not(.init)", function() {
        placeOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#place").children('.init').html($(this).html());
        placeOptions.toggle('slow');
    });


    var bankOptions = $("#bank").children('li:not(.init)');
    $("#bank").on("click", "li:not(.init)", function() {
        bankOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#bank").children('.init').html($(this).html());
        bankOptions.toggle('slow');
    });

    var activityOptions = $("#activity").children('li:not(.init)');
    $("#activity").on("click", "li:not(.init)", function() {
        activityOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#activity").children('.init').html($(this).html());
        activityOptions.toggle('slow');
    });

    var memberOptions = $("#member").children('li:not(.init)');
    $("#member").on("click", "li:not(.init)", function() {
        memberOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#member").children('.init').html($(this).html());
        memberOptions.toggle('slow');
    });

    $('#signup-form').validate({
        rules : {
            first_name : {
                required: true,
            },
            last_name : {
                required: true,
            },
            phone_number : {
                required: true
            },
            password : {
                required: true
            },
            re_password : {
                required: true,
                equalTo: "#password"
            }
        },
        onfocusout: function(element) {
            $(element).valid();
        },
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });
})(jQuery);
