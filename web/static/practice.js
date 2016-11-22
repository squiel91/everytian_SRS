favorite = false;

function explain(word, pronunciation, definitions){
	$( ".explain-box .word" ).text(word);
	$( ".explain-box .pronunciation" ).text(pronunciation);
	def_list = $( ".explain-box .definition" ).empty();
	for(var i = 0; i < definitions.length; i++){
		def_list.append("<li>" + definitions[i] + "</li>");	
	}
	$("#corrector").height($( ".explain-box").height());
}

var last_touched="";

function clear_explain(){
	$( ".explain-box .word" ).empty();
	$( ".explain-box .pronunciation" ).empty();
	$( ".explain-box .definition" ).empty();
	$("·corrector").height($( ".explain-box").height());
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

$( "#translate" ).click(function(event) {
  if(event.target.innerHTML == 'Translate') {
  	$("#translation").show();
  	event.target.innerHTML = "Hide translation";
  } else {
  	$("#translation").hide();
  	event.target.innerHTML = 'Translate';
  }
});

$( "#favorite" ).click(function(event) {
  if(event.target.innerHTML == 'Favorite') {
  	favorite = true;
  	$(this).text("Remove favorite");
  	$(this).next().prop('checked', true);
  } else {
  	favorite = false;
  	$(this).next().prop('checked', false);
  	$(this).text("Favorite");
  }
});