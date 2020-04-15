$(document).ready(function() {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });

    $(document).ajaxError(function(e, xhr) {
        var message = null;

        if (xhr.responseJSON && xhr.responseJSON.hasOwnProperty('message')) {
            message = xhr.responseJSON.message;
        } else if (xhr.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(xhr.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(xhr.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        Materialize.toast({html: message});
    });



    $(window).bind('hashchange', function() {
        // hash #intro, #blessing
        var hash = window.location.hash.replace('#', '');
        var url = null;

        if (hash === 'bless') {
            url = bless_page_url; //如果hash为#blessing
        } else {
            url = intro_page_url; //如果hash为#intro
        }

        $.ajax({
            async: true,
            type: 'GET',
            url: url,
            success: function(data) {
                $('#main').hide().html(data).fadeIn(600); //将返回的局部页面插入到main元素中
                activeComponent();
            }
        });
    });

    //激活插入页面的Materiallize组件
    function activeComponent() {
        $('.button-collapse').sideNav();
        $('.parallax').parallax();
    }

    if (window.location.hash === '') {
        window.location.hash = '#intro'; // 默认状态， 或者第一次访问
    } else {
        $(window).trigger('hashChange'); // 当用户刷新页面，或者访问带有hash的URL， 触发hashChange事件
    }


    // 创建新的Bless
    function new_item(e) {
        var $input = $('#bless-input');
        var body = $input.val().trim();

        //如果不是按下回车键，或者没有body，则取消
        if (e.which != ENTER_KEY || !body) {
            return;
        }
        $input.focus().val('');
        $.ajax({
            type: 'POST',
            url: new_bless_url,
            data: JSON.stringify({'body': body}),
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {
                Materialize.toast({html: data.message, classes: 'rounded'});
                $('#items').prepend(data.html);
                $('#bless-count').text(data.bless_count);
                $('.button-collapse').sideNav();
            }
        });
    }

    // bless-input输入框绑定keyup时间
    $(document).on('keyup', '#bless-input', new_item.bind(this));












});