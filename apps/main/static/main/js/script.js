$(document).ready(function(){

    // index.html

    $("#sign-in").click(function() {
        $.ajax({
            url: '/login',
            success: function(serverResponse) {
                $('#form').html(serverResponse)
                $('#log_reg').html("Don't have an account? Register <button id='register' class='btn-clear text-danger'>here</button>.")
            }
        });
        $('html,body').animate({
            scrollTop: $("#form").offset().top}, 'slow');
    });

    $("#sign-up").click(function() {
        $.ajax({
            url: '/register',
            success: function(serverResponse) {
                $('#form').html(serverResponse)
                $('#log_reg').html("Already have an account? Sign-in <button id='login' class='btn-clear text-danger'>here</button>.")
            }
        });
        $('html,body').animate({
            scrollTop: $("#form").offset().top}, 'slow');
    });

    $(document).on('click', '#register', function(){
        $.ajax({
            url: '/register',
            success: function(serverResponse) {
                $('#form').html(serverResponse)
                $('#log_reg').html("Already have an account? Sign-in <button id='login' class='btn-clear text-danger'>here</button>.")
            }
        });
    });

    $(document).on('click', '#login', function(){
        $.ajax({
            url: '/login',
            success: function(serverResponse) {
                $('#form').html(serverResponse)
                $('#log_reg').html("Don't have an account? Register <button id='register' class='btn-clear text-danger'>here</button>.")
            }
        });
    });

    $(document).on('click', '#check_registration', function(){
        if ( $('#reg_username').val().length < 3 ) {
            $('#reg_errors').html('<small>Invalid username.<small>');
            return false
        } 
        else if ( $('#reg_email').val().length === 0) {
            $('#reg_errors').html('<small>Invalid email.<small>');
            return false
        }
        else if ( $('#reg_password').val().length < 8 ) {
            $('#reg_errors').html('<small>Invalid password.<small>');
            return false
        }
        else if ( $('#reg_password').val() != $('#confirm_password').val() ) {
            $('#reg_errors').html('<small>Passwords do not match.<small>');
            return false
        }
    })

    $(document).on('click', '#check_login', function(){
        if ( $('#log_username').val().length < 3 ) {
            $('#log_errors').html('<small>Invalid username.<small>');
            return false
        } 
        else if ( $('#log_password').val().length < 8 ) {
            $('#log_errors').html('<small>Invalid password.<small>');
            return false
        }
    })

    // home.html

    $(document).on('click', '#new_question', function(){
        $.ajax({
            url: '/new_question',
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    })

    $(document).on('click', '#respond', function(){
        var add_response = $(this).parent().attr('action')
        var question_id = $(this).attr('ref')
        $.ajax({
            url: add_response,
            method: 'POST',
            data: $(this).parent().serialize(),
            success: function(serverResponse) {
                $('#'+question_id).html(serverResponse)
            }
        });
        return false
    });

    $(document).on('click', '#check_question', function(){
        if ( $('#question_input').val().length === 0 ) {
            $('#new_question_errors').html('Question field cannot be blank.');
            return false
        }
    });

    $(document).on('click', '#check_response', function(){
        if ( ($('#response_input').val().length === 0) && ($('#textbox').val().length === 0) ) {
            $('#new_response_errors').html('<p>Cannot give a blank response.</p>');
            return false
        }
    });

    $('.dropdown-item').hover(
        function() {
            $(this).removeClass('text-white')
            $(this).addClass('hover-1')
        },
        function() {
            $(this).removeClass('hover-1')
            $(this).addClass('text-white')
        }
    )

    // my_questions.html

    $(document).on('click', '#new_question', function(){
        $.ajax({
            url: '/new_question',
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    });

    $('#delete').click(function(){
        $.ajax({
            url: '/delete_question',
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    })

    // question.html

    $('#respond').click(function(){
        var add_response = $(this).parent().attr('action')
        var question_id = $(this).attr('ref')
        $.ajax({
            url: add_response,
            method: 'POST',
            data: $(this).parent().serialize(),
            success: function(serverResponse) {
                $('#'+question_id).html(serverResponse)
            }
        });
        return false
    });

    // questions.html

    $(document).on('click', '#new_question', function(){
        $.ajax({
            url: '/new_question',
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    })

    $(document).delegate('#textbox', 'keydown', function(e) {
        var keyCode = e.keyCode || e.which;

        if (keyCode == 9) {
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;

            $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end)
            );
            
            this.selectionStart =
            this.selectionEnd = start + 1;
        }
    });

    $(document).on('click', '#respond', function(){
        var add_response = $(this).parent().attr('action')
        var question_id = $(this).attr('ref')
        $.ajax({
            url: add_response,
            method: 'POST',
            data: $(this).parent().serialize(),
            success: function(serverResponse) {
                $('#'+question_id).html(serverResponse)
            }
        });
        return false
    });

    $(document).on('click', '#browse', function(){
        $.ajax({
            url: '/browse',
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        })
    });

    $(document).on('keyup', '#search', (function(e) {
        console.log('value: ', $('#search').serialize());
        $.ajax({
            method: "POST",
            url: "/search_question",
            data: $('#search').parents().serialize(),
            success: function(response) {
                $('#browse_results').html(response);

            }
        })
    }));

    $('.dropdown-item').hover(
        function() {
            $(this).removeClass('text-white')
            $(this).addClass('hover-1')
        },
        function() {
            $(this).removeClass('hover-1')
            $(this).addClass('text-white')
        }
    )

    // profile.html

    $('#user_questions').click(function(){
        var link = '/user_questions/' + $(this).attr('ref')
        $.ajax({
            url: link,
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    })

    $('#user_responses').click(function(){
        var link = '/user_responses/' + $(this).attr('ref')
        $.ajax({
            url: link,
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    })

    $('#user_following').click(function(){
        var link = '/user_following/' + $(this).attr('ref')
        $.ajax({
            url: link,
            success: function(serverResponse) {
                $('#content_area').html(serverResponse)
            }
        });
    })

})