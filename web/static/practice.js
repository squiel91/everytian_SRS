// initialize menu

$("nav #twitter").click(function(){
	window.open('https://twitter.com/intent/tweet?url=http://everytian.com&hashtags=chinese&text=' + $('.text').data('string'), '_blank');
})

$("nav #edit").click(function(){
	if($(this).hasClass('active')){ 
		$('#finish').hide();
		$('#continue-edition').hide();
		$('#confirm').hide();
		$('.slick-active').find('.text').attr('contenteditable','false');
		$('.slick-active').find('#translation').attr('contenteditable','false');
		$('.slick-active').find('.text').data('string', $('.slick-active').find('.text').data('backup'));
		var words = $('.slick-active').find('.text').data('backup').split(' ');
			show_words(words, $('.slick-active').find('.text'));
		$(this).removeClass('active');
	} else { 
		clear_explain();
		$(this).addClass('active'); 
		$('.slick-active').find('.text').text($('.slick-active').find('.text').data('string'));  
		$('.slick-active').find('.text').attr('contenteditable','true');  
		$('.slick-active').find('.translation').attr('contenteditable','true'); 
		$('#confirm').hide();
		$('#finish').show();
		$('#cancel').show();
		$(this).addClass('active')
	}
})

$("nav #sound").click(function(){
	if($(this).hasClass('active')){ 
		$(this).removeClass('active'); 
		$('.slick-active').find('audio')[0].pause(); 
		$('audio')[0].currentTime = 0;
	} else { 
		$(this).addClass('active'); 
		$('.slick-active').find('audio')[0].play(); 
		var sound_button = $(this); 
		$('.slick-active').find('audio').on('ended', function(){ 
			sound_button.removeClass('active');
		});
	};
})

$("nav #favorite").click(function(){
	if($(this).hasClass('active')){ 
		$(this).removeClass('active');
		is_favorite = false;
	} else { 
		$(this).addClass('active')
		is_favorite = true;
	};
})

$("nav #translate").click(function(){
	if(!$(this).hasClass('active')){ 
		$('.slick-active').find('.translation').show(); 
		$(this).addClass('active');
	} else { 
		$('.slick-current').find('.translation').hide(); 
		$(this).removeClass('active');
	};
})

$("nav #ask").click(function(){
	if($(this).hasClass('active')){
		$(this).removeClass('active');
		$('.slick-active').find('#question').hide()
	} else { 
		$('.slick-active').find('#question').show()
		$(this).addClass('active')     
	};
})

// initialize global variables

var dict = {};
var unknown_words = {};
var id_to_process = [];
first_resource = true;
current_slide_index = 0;
added_slicks = 0;
is_favorite = false;
requested_resource_id = window.location.pathname.split("/")[2];

// initialize explain

$( ".explain" ).draggable({ axis: "y" });

// initialize carousel

$("#carru").slick({
	speed: 300,
	accessibility: false,
	arrows: false,
	infinite: false
});

if(requested_resource_id) {
	get_next(requested_resource_id);
} else {
	get_next();
}

$('#carru').on('afterChange', function next_resource(event, slick, currentSlide){
	clear_explain();
	if(current_slide_index + 2 <= currentSlide){
		$('#translate').removeClass('active');
		$('#favorite').removeClass('active');
		$('#sound').removeClass('active');
		$('#ask').removeClass('active');
		$('#edit').removeClass('active');
		$("#carru").slick('slickRemove', 0);
		$("#carru").slick('slickRemove', 0);
		
		window.history.replaceState("object or string", "Title", practice_url + "/" + $(".slick-current").data("id"));
		get_next();
	}
});

function get_next(resource_id) {
	request_url = base_url;
	
	if(!(resource_id  === undefined)){
		request_url = request_url + "/" + resource_id;
	}
	unknown_words_list = [];
	var send_json = {};
	send_json["email"] = user_email;
	if(id_to_process.length > 1) {
		send_json["resource_id"] = id_to_process.shift();
		send_json["favorite"] = is_favorite;
		for (var word in unknown_words) {
    		var unknown = unknown_words[word];
    		if(unknown){
    			unknown_words_list.push(word);
    		}
		}
		send_json["unknown_words"] = unknown_words_list
		unknown_words = {}
	}

	$.get( request_url, send_json ,function( data ) {
		console.log(data);
		var resource = $('<div class="resource drag"></div>');
		var sound = $('<div class="sound"></div>');
		var text = $('<div class="text"></div>');
		var translation = $('<div class="translation"></div>');

		
		var edit = $('<button id="continue-edition">Edit</button>').hide().click(function(evt) {
			edit.hide();
			$(evt.target).hide();
			text.text(text.data("string"));
			text.attr('contenteditable','true');
			translation.attr('contenteditable','true');
			// deactivate draggable
			confirm.hide();
			finish.show();
		});

		var finish = $('<button id="finish">Finish</button>').hide().click(function(evt) {
			finish.hide();
			text.data("string", text.text());
			var words = text.text().split(' ');
			show_words(words, text);
			get_definitions(words, dict);
			text.attr('contenteditable','false');
			translation.attr('contenteditable','false');
			edit.show();
			// activate draggable
			confirm.show();
		});

		var confirm = $('<button id="confirm">Confirm</button>').hide().click(function(evt) {
				new_text = {
					"text": text.data("string").split(' '),
					"translation": translation.text(),
					'csrfmiddlewaretoken': $( "[name='csrfmiddlewaretoken']" ).val()
				}
				confirm.text("Sending...")
			$.post(base_url + '/' + resource.data("id"), new_text, function(response) {
				confirm.hide();
				confirm.text("Confirm")
				edit.hide()
				$('#edit').removeClass('active');

			}, 'json');
		});

		var question = $('<div id="question"><h2>You will soon be able to ask questions to a techer!</h2></div>').hide()


		resource.append(text).append(sound).append(translation);
		resource.append(edit).append(finish).append(confirm).append(question);

		resource.data("id", data["id"]);
		id_to_process.push( data["id"]);
		text.data("string", data["text"].join(" "));
		text.data("backup", data["text"].join(" "));
		words = data["words"];
		for(i in words){
			dict[words[i]['hanzi']] = {
				'pronunciation': words[i]['pinyin'],
				'definitions': words[i]['definitions']
			}
		}
		show_words(data["text"], text, dict);
		translation.text(data["translation"]);
		if(data["audio"]){
			sound.append('<audio><source src="https://audio.tatoeba.org/sentences/cmn/' + data["audio"] + '.mp3" type="audio/mpeg">Your browser does not support audio!</audio>');
		}
		if(added_slicks > 0){
			
		}
		if(first_resource){
			window.history.replaceState("object or string", "Title", practice_url + "/" + data["id"]);
			first_resource = false;
			get_next();
		}
		$("#carru").slick('slickAdd', resource);
		added_slicks += 1;
		$("#carru").slick('slickAdd', "<div></div>");
		added_slicks += 1;

		resource.css("min-height", $(window).height() - $('nav').height());
	}, 'json');
}

function show_words(words, jQ_div, dict){
	jQ_div.empty();
	for(i in words) {
		word = words[i]
		new_word = $('<span class="word">'+ word + '</span>').click(on_word_click);
		jQ_div.append(new_word);
	};
}

function get_definitions(words, dictionary){
	var punctuation = '…！？／（）、，。：「」…『』！？《》“”；’ ‘【】·〔〕.,?!-[]';
	for(i in words) { 
		if (!dictionary[words[i]] && !punctuation.includes(words[i])) {
			$.getJSON( words_url + "/" + words[i], function(word) {
				if(word['hanzi']){
					dictionary[word['hanzi']] = {
						'pronunciation': word['pinyin'],
						'definitions': word['definitions']
					}
				} else {
					console.log(word['warning']);
				}
			});
		}
	}
}

// Explain

function explain(word, pronunciation, definitions){
	$( ".explain" ).animate({top: $(window).height()}, 200, function(){
		$( ".explain" ).show()
		$( ".explain .word" ).text(word);
	$( ".explain .pronunciation" ).text(pronunciation);
	def_list = $( ".explain .definition" ).empty();
	for(var i = 0; i < definitions.length; i++){
		def_list.append("<li>" + definitions[i] + "</li>"); 
	};
		$( ".explain" ).animate({top: $(window).height() - 170}, 200);
	})
}

var last_touched="";

function clear_explain(){
	$( ".explain" ).animate({top: $(window).height()}, 200)
}

function on_word_click(event) {
	touched_word = $(this).text()
	if(touched_word in dict) {
		if (last_touched == touched_word){
			if ($(this).hasClass( "unknown" )){
				$(this).removeClass( "unknown" );
				unknown_words[touched_word] = false;
				console.log(unknown_words); 
				clear_explain();
			} else {
				word_dict = dict[touched_word];
				explain(touched_word, word_dict["pronunciation"], word_dict["definitions"]);
				$(this).addClass( "unknown" );
				unknown_words[touched_word] = true;
				console.log(unknown_words); 
			}
		} else {
			word_dict = dict[touched_word];
			explain(touched_word, word_dict["pronunciation"], word_dict["definitions"]);
			if (!$(this).hasClass("unknown")){
				$(this).addClass("unknown");
				unknown_words[touched_word] = true;
				console.log(unknown_words); 
			}
		};
		last_touched = touched_word;
	}
};
