$(document).ready(function() {

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



    $(window).bind('hashChange', function() {
        // hash #intro, #blessing
        var hash = window.location.hash.replace('#', '');
        var url = null;

        if (hash === 'blessing') {
            url = blessing_page_url; //如果hash为#blessing
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




});