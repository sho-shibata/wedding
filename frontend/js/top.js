const baseUrl = 'https://s-wedding-invitation.com/api/';
// const baseUrl = 'http://localhost/api/';

$(function(){
    $('html,body').animate({ scrollTop: 0 }, '1');
    countDownDays();

    // $('#attend-1, #attend-2').click(checkAttendence);
})

// カウントダウン
const countDownDays = function(){
    // 今日の日付
    let date1 = new Date(Date.now());

    // 2023/6/4
    let date2 = new Date(2023, 5, 4);

    // 差分
    let diffTime = date2 - date1;
    let diffDay = Math.floor(diffTime / (1000 * 60 * 60 * 24)) + 1;

    $('.left-days').text(diffDay);
}


const checkAttendence = function(){
    let isAttend = $('#attend-1').prop('checked');
    if(isAttend){
        $('#attend-1-label').addClass('hand-writing-border');
        $('#attend-2-label').removeClass('hand-writing-border');
        $('.attend-anime').css('display', 'block');
    }else{
        $('#attend-2-label').addClass('hand-writing-border');
        $('#attend-1-label').removeClass('hand-writing-border');
        $('.attend-anime').css('display', 'none');
    }
}

// 送信ボタン押下
const clickSubmitBtn = async function(){
    $('.wedding-invitation-btn').prop('disabled', true);
    // 入力データを取得
    inputData = createDataSet();

    // 通信
    let data = await execAjax('POST', 'register', inputData);

    if(data.result == 'success'){
        window.location.href = '/thankyou'
    }else{
        dispMessage(data.data.messages);
        $(window).scrollTop($('.wedding-invitation').position().top);
    }
    $('.wedding-invitation-btn').prop('disabled', false);
}

// データセット作成
const createDataSet = function(){
    let dataSet = {}
    // 出席確認
    dataSet['attendance'] = $('#attend-1').prop('checked') ? '1' : $('#attend-2').prop('checked') ? '0' : '';
    // 招待側
    dataSet['invitation_side'] = $('#invitation-from-1').prop('checked') ? '1' : '0';
    // 関係
    dataSet['relationship'] = $('#relationship-1').val();
    // 名前（姓）
    dataSet['last_name'] = $('#last-name').val();
    // 名前（名）
    dataSet['first_name'] = $('#first-name').val();
    // 名前フリガナ（姓）
    dataSet['last_name_kana'] = $('#last-name-kana').val();
    // 名前フリガナ（名）
    dataSet['first_name_kana'] = $('#first-name-kana').val();
    // 性別
    let gender = $('#gender-1').prop('checked') ? '1' : 
                    $('#gender-2').prop('checked') ? '2' :
                    $('#gender-3').prop('checked') ? '3' : '';
    dataSet['gender'] = gender;
    // 郵便番号
    dataSet['zip_code'] = $('#zip-code').val();
    // 住所
    dataSet['address'] = $('#address').val();
    // メールアドレス
    dataSet['email'] = $('#email').val();
    // アレルギー
    dataSet['allergy'] = $('#allergy').val();
    // メッセージ
    dataSet['message'] = $('#message').val();
    
    return dataSet;
}

// ajax通信
const execAjax = function(method, url, sendData, loadFlg = 1){
    // ロード中画面開始
    if (loadFlg == 1){
        buildLoading();
        $(document).ajaxSend(function() {
            $("#overlay").fadeIn(300);　
        });
    }else{
        $("#overlay").remove();
    }
    
    // 送信するデータをjson化
    let jsonData = JSON.stringify(sendData);

    return new Promise((resolve) => {
        // 非同期処理
        $.ajax({
            type: method,
            url: baseUrl + url,
            contentType : "application/json; charset=utf-8",
            xhrFields: { withCredentials: true },
            dataType: 'json', // データをjson形式で飛ばす
            data: jsonData
        })
        .done(function(data) {
            // ロード中画面終了
            if (loadFlg == 1){
                setTimeout(function(){
                    $("#overlay").fadeOut(300);
                },500);    
            }
            // ajax成功
            if(data.result == 'success'){
                // 処理成功の場合
                resolve(data);
            }else{
                // 処理失敗の場合
                resolve(data);
            }
        })
        .fail(function(data) {
            // ロード中画面終了
            if (loadFlg == 1){
                setTimeout(function(){
                    $("#overlay").fadeOut(300);
                },500);    
            }
            $('.wedding-invitation-btn').prop('disabled', false);        
            // ajax失敗
            alert('エラー:通信失敗');
        });
    })
}

// ロード中画面
const buildLoading = function(){
    if (!$('#overlay').length){
        let loading = '';
        loading += '<div id="overlay">';
        loading += '    <div class="cv-spinner">';
        loading += '        <span class="spinner"></span>';
        loading += '    </div>';
        loading += '</div>';
        $('.outside-container').append(loading);
    }
}

// エラーメッセージ表示
const dispMessage = function(messages){
    let dispMessage = '';
    $('.error-message').empty();
    $.each(messages, function(index, message){
        dispMessage += '<p class="color-red">' + message + '</p>';
    })
    $('.error-message').append(dispMessage);
}