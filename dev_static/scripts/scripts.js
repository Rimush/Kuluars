$scroll_last = 0;

$(document).ready(function(){

	$('.b-abc__item').click(function() {
		$('.b-abc__item').removeClass('b-abc__item--active');
		$(this).addClass('b-abc__item--active');
		if ($(this).attr('data-word') == 'all') {
			$('.b-tags__list-link').show();
		} else {
			$('.b-tags__list-link[data-word!=' + $(this).attr('data-word') + ']').hide();
			$('.b-tags__list-link[data-word=' + $(this).attr('data-word') + ']').show();
		}
	});
	
	$('.b-tags__list-link').each(function(){
		$word = $(this).data('word');
		$('.b-abc__item[data-word=' + $word + ']').removeClass('b-abc__word-disable').addClass('b-abc__word');
	});
	
	$word_current = $('.b-sub-page-articles__header').data('word');
	if ($word_current != '') {
		$('.b-abc__item').removeClass('b-abc__item--active');
		$('.b-abc__item[data-word=' + $word_current + ']').addClass('b-abc__item--active');
		$('.b-tags__list-link[data-word!=' + $word_current + ']').hide();
		$('.b-tags__list-link[data-word=' + $word_current + ']').show();
	} else {
		$('.b-abc__item[data-word=all]').addClass('b-abc__item--active');
	}
	
	/*$.ajax({
		url: "http://127.0.0.1:8000/api/tags/",
		cache: false
	}).done(function( html ) {
		console.log(html);
	}); */	
	
	/*$(window).scroll(function(){
		$top = $(window).scrollTop();
		if ($top > $('.b-header').height()) {
			$('.b-menu').addClass('b-menu--fixed');
			$('.b-content').addClass('b-content--fixed');
			
		} else {
			$('.b-menu').removeClass('b-menu--fixed');
			$('.b-content').removeClass('b-content--fixed');
		}
		
		if ($scroll_last < $top && $top > ($('.b-header').height() * 2)) {
			$('.b-menu').slideUp(300);
		}
		
		if ($scroll_last > $top) {
			$('.b-menu').slideDown(300);
		}
		
		$scroll_last = $top;
	});*/

	$('.b-to-top').click(function() {
		$('html, body').animate({scrollTop: 0},1000);
		return false;
	})

	$('.b-menu-search-button').click(function() {
		$('.b-menu-search-input').removeClass('b-menu-search-input--hide');
		$('.b-menu-search-button').addClass('b-menu-search-button--black');
		$('.b-menu-search-input').focus();
	})
	$(document).mouseup(function(e) {
		var $block = $('.b-menu-search');
		if (!$block.is(e.target) && $block.has(e.target).length === 0) {
			$('.b-menu-search-input').addClass('b-menu-search-input--hide');
			$('.b-menu-search-button').removeClass('b-menu-search-button--black');
			$('.b-menu-search-input').val('');
		}
	});
	
	$('.comment-popup-open').click(function() {
		$('.comment-popup-fade').fadeIn();
		return false;
	});	
	
	$('.comment-popup-close').click(function() {
		$(this).parents('.comment-popup-fade').fadeOut();
		return false;
	});		
 
	$(document).keydown(function(e) {
		if (e.keyCode === 27) {
			e.stopPropagation();
			$('.comment-popup-fade').fadeOut();
		}
	});
	
	$('.comment-popup-fade').click(function(e) {
		if ($(e.target).closest('.comment-popup').length == 0) {
			$(this).fadeOut();					
		}
	});
	
	$('.b-sub-page-article-content__text img').each(function(i, elem) {
		$width = $(elem).width();
		$height = $(elem).height();
		$(elem).width('100%');
		$(elem).height($(elem).width() / $width * $height);
	});
});