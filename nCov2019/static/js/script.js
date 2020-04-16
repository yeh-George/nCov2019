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

                setTimeout(toggle_btn(), 601); //因为fadeIn需要600，toggle_btn需要在内容加载完后实现
            }
        });
    });

    //实现当hash变化时，toggle-btn的内容和href也相应变化
    function toggle_btn() {
        var $btn = $('#toggle-btn');

        if (window.location.hash === '#bless') {
            $btn.text('返回主页');
            $btn.attr('href', '#intro');
        } else {
            $btn.text('发送祝福');
            $btn.attr('href', '#bless');
        }

    }

    //激活插入页面的Materiallize组件
    function activeComponent() {
        $('.button-collapse').sideNav();
        $('.parallax').parallax();
    }

    if (window.location.hash === '') {
        window.location.hash = '#intro'; // 默认状态， 或者第一次访问
    } else {
        $(window).trigger('hashchange'); // 当用户刷新页面，或者访问带有hash的URL， 触发hashChange事件
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

    // bless-input输入框绑定keyup事件
    $(document).on('keyup', '#bless-input', new_item.bind(this));

    // 按下ESC清除内容
    function clear_body(e) {
        var $input = $('#bless-input');

        if (e.which === ESC_KEY) {
            $input.focus().val('');
        }

    }

    $(document).on('keydown', '#bless-input', clear_body.bind(this));


    // pagination组件 实现换页
    function paginate_bless(e) {
        var $el = $(e.target);

        $.ajax({
            type: 'GET',
            url: bless_page_url,
            data: {'page': $el.data('page')},
            success: function(data) {
                $('#main').hide().html(data).fadeIn(600); //将返回的局部页面插入到main元素中
                activeComponent();
                setTimeout(toggle_btn(), 601); //因为fadeIn需要600，toggle_btn需要在内容加载完后实现
                $('#bless-input').focus();
            }
        });

    }

    // 点击分页组件
    $(document).on('click', '.page', paginate_bless.bind(this));

    // 刷新按钮 （可以直接用paginate_bless方法
    function refresh_bless(e) {
        $.ajax({
            type: 'GET',
            url: bless_page_url,
            success: function(data) {
                $('#main').hide().html(data).fadeIn(600); //将返回的局部页面插入到main元素中
                activeComponent();
                setTimeout(toggle_btn(), 601); //因为fadeIn需要600，toggle_btn需要在内容加载完后实现
                $('#bless-input').focus();
            }
        });
    }

    $(document).on('click', '#refresh-btn', refresh_bless.bind(this));


    // 点赞按钮
    function thumb_up(e) {
        var $el = $(e.target);
        var id = $el.data('id');

        $.ajax({
            type: 'GET',
            url: thumb_up_url,
            data: {'id': id},
            success: function(data) {
                $('#thumb-up-' + id).text(data.num);
                Materialize.toast({html: data.message, classes: 'rounded'});
            }
        });
    }

    $(document).on('click', '.thumb-up', thumb_up.bind(this));


















});