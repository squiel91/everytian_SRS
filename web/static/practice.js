favorite = false;

$( ".explain-box" ).draggable({ axis: "y" });

function explain(word, pronunciation, definitions){
  $( ".explain-box").hide();

	$( ".explain-box .word" ).text(word);
	$( ".explain-box .pronunciation" ).text(pronunciation);
	def_list = $( ".explain-box .definition" ).empty();
	for(var i = 0; i < definitions.length; i++){
		def_list.append("<li>" + definitions[i] + "</li>");	
	};

  $( ".explain-box").show();
	$("#corrector").height($( ".explain-box").height());
}

var last_touched="";

function clear_explain(){
	$( ".explain-box .word" ).empty();
	$( ".explain-box .pronunciation" ).empty();
	$( ".explain-box .definition" ).empty();
  $( ".explain-box").hide();
	$("#corrector").height(0);
}

$( ".hanzi" ).click(function(event) {
  touched_word = $(this).text()
  if(touched_word in dict) {
  	if (last_touched == touched_word){
  		if ($(this).hasClass( "unknown" )){
  			$(this).removeClass( "unknown" );
  			$(this).next().prop('checked', false).next().hide();
  			clear_explain();
  		} else {
  			word_dict = dict[touched_word];
  			explain(touched_word, word_dict["pinyin"], word_dict["definitions"]);
  			$(this).addClass( "unknown" );
  			$(this).next().prop('checked', true).next().show();
  		}
  	} else {
  		word_dict = dict[touched_word];
  		explain(touched_word, word_dict["pinyin"], word_dict["definitions"]);
  		if (!$(this).hasClass("unknown")){
  			$(this).addClass("unknown");
  			$(this).next().prop('checked', true).next().show();
  		}
  	};
  	last_touched = touched_word;
  }
});

$( "#sound" ).click(function(event) {
  $("audio")[0].play();
});

$( "#translate" ).click(function(event) {
  // if(event.target.innerHTML == 'Translate') {
  	$("#translation").toggle();
  // 	event.target.innerHTML = "Hide translation";
  // } else {
  // 	$("#translation").hide();
  // 	event.target.innerHTML = 'Translate';
  // }
});

$( "#favorite" ).click(function(event) {
  if(!favorite) {
  	favorite = true;
  	$(this).next().prop('checked', true);
  } else {
  	favorite = false;
  	$(this).next().prop('checked', false);
  }
});