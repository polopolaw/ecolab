;(function($){

	'use strict';

	$(function(){

		/* ---------------------------------------------------- */
		/*	Sticky spacer										*/
		/* ---------------------------------------------------- */

		$('#header').after('<div class="sticky-spacer"></div>');

		if ($('.sticky-spacer').length){

			$(window).on("load resize",function(){

				$('.sticky-spacer').css({'height': $('#header').outerHeight()});

				$('.sticky-spacer').hide();

			});

		}

		/* ---------------------------------------------------- */
		/*	Revolution slider									*/
		/* ---------------------------------------------------- */

	    if ($('#header').hasClass('header-abs')) {

	    	if ($('#rev-slider').length) {
				jQuery("#rev-slider").revolution({
		            sliderType:"standard",
			    	spinner: "spinner3",
			    	responsiveLevels: [4096,1024,778,480],
			    	delay:6000,
		            navigation: {
		                arrows:{
		                	enable:true,
		                	left: {
								container:"slider",
					            h_align:"left",
					            v_align:"center",
					            h_offset:30,
					            v_offset:0
							},
							right: {
					            container:"slider",
					            h_align:"right",
					            v_align:"center",
					            h_offset:30,
					            v_offset:0
							}
		                },
		                bullets:{
				        	style:"",
				        	enable: false,
				        	container: "slider",
				        	hide_onmobile: false,
				        	hide_onleave: false,
				        	hide_delay: 200,
				        	hide_under: 0,
				        	hide_over: 9999,
				        	tmp:'<span class="circle-bullet"></span>', 
				        	direction:"horisontal",
				        	space: 10,       
				        	h_align: "center",
				        	v_align: "bottom",
				        	v_offset: 20
				        }
		            },
		            gridwidth:1170,
		            gridheight:1035
		        });

		    }

		}

		else{

			if ($('#rev-slider').length) {
				jQuery("#rev-slider").revolution({
		            sliderType:"standard",
			    	spinner: "spinner3",
			    	responsiveLevels: [4096,1024,778,480],
			    	delay:6000,
		            navigation: {
		                arrows:{
		                	enable:true,
		                	left: {
								container:"slider",
					            h_align:"left",
					            v_align:"center",
					            h_offset:30,
					            v_offset:0
							},
							right: {
					            container:"slider",
					            h_align:"right",
					            v_align:"center",
					            h_offset:30,
					            v_offset:0
							}
		                },
		                bullets:{
				        	style:"",
				        	enable: false,
				        	container: "slider",
				        	hide_onmobile: false,
				        	hide_onleave: false,
				        	hide_delay: 200,
				        	hide_under: 0,
				        	hide_over: 9999,
				        	tmp:'<span class="circle-bullet"></span>', 
				        	direction:"horisontal",
				        	space: 10,       
				        	h_align: "center",
				        	v_align: "bottom",
				        	v_offset: 20
				        }
		            },
		            gridwidth:1170,
		            gridheight:730
		        });

		    }

		}

		/* ---------------------------------------------------- */
        /*	Gallery carousel									*/
        /* ---------------------------------------------------- */

	  	var pageCarousel = $('.owl-carousel');

		if(pageCarousel.length){

			$('.owl-carousel').not('#thumbnails').each(function(){
	
				/* Max items counting */
				var max_items = $(this).data('max-items');
				var tablet_items = max_items;
				if(max_items > 1){
					tablet_items = max_items - 1;
				}
				var mobile_items = 1;

				var autoplay_carousel = $(this).data('autoplay');

				var center_carousel = $(this).data('center');

				var item_margin = $(this).data('item-margin');
				
				/* Install Owl Carousel */
				$(this).owlCarousel({
				    smartSpeed : 450,
				    nav : true,
				    loop  : true,
				    autoplay : autoplay_carousel,
				    center: center_carousel,
				    autoplayTimeout: 3000,
				    navText : false,
				    margin: item_margin,
				    lazyLoad: true,
				    rtl: $.mad_core.SUPPORT.ISRTL ? true : false,
				    responsiveClass:true,
				    responsive : {
				        0:{
				            items:mobile_items
				        },
				        481:{
				            items:tablet_items
				        },
				        992:{
				            items:max_items
				        }
				    }
				});


			});

			$('.custom-owl-prev').on('click',function(){

				$('.owl-carousel').trigger('prev.owl.carousel');

				return false;

			});

			$('.custom-owl-next').on('click',function(){

				$('.owl-carousel').trigger('next.owl.carousel');

				return false;

			});

			if($('#thumbnails').length){
				$('#thumbnails').each(function(){
					
					$(this).owlCarousel({
						items : 4,
						URLhashListener : false,
						navSpeed : 800,
						margin: 10,
						dots: false,
						nav : true,
						loop : true,
						rtl: $.mad_core.SUPPORT.ISRTL ? true : false,
						navText:false,
						responsive : {
					        0:{
					            items:2
					        },
					        481:{
					            items:4
					        }
					    }
				    });
				});
			    
			}
		}

		/* ---------------------------------------------------- */
		/*	Elevate zoom										*/
		/* ---------------------------------------------------- */

		if($('[data-zoom-image]').length){

			var button = $('.fancybox');

			$("#zoom-image").elevateZoom({
				gallery:'thumbnails',
				galleryActiveClass: 'active',
				zoomType: "inner",
				cursor: "crosshair",
				responsive:true,
			    zoomWindowFadeIn: 500,
				zoomWindowFadeOut: 500,
				easing:true,
				lensFadeIn: 500,
				lensFadeOut: 500
			});

			button.on("click", function(e){
			    var ez = $('#zoom-image').data('elevateZoom');
				$.fancybox(ez.getGalleryList());
			  	e.preventDefault();
			});

		}

		/* ---------------------------------------------------- */
        /*	SmoothScroll										*/
        /* ---------------------------------------------------- */

		try {
			$.browserSelector();
			var $html = $('html');
			if ( $html.hasClass('chrome') || $html.hasClass('ie11') || $html.hasClass('ie10') ) {
				$.smoothScroll();
			}
		} catch(err) {}

		/* ---------------------------------------------------- */
        /*	Custom Select										*/
        /* ---------------------------------------------------- */

		if ($('.custom-select').length) {
			$('.custom-select').madCustomSelect();
		}

		/* ---------------------------------------------------- */
        /*	Tabs												*/
        /* ---------------------------------------------------- */

        $(window).on("load",function(){

        	var tabs = $('.tabs-section');
			if(tabs.length){
				tabs.tabs({
					beforeActivate: function(event, ui) {
				        var hash = ui.newTab.children("li a").attr("href");
				   	},
					hide : {
						effect : "fadeOut",
						duration : 450
					},
					show : {
						effect : "fadeIn",
						duration : 450
					},
					updateHash : false
				});
			}

			if($('ul.smooth_tabs').length){
				$('ul.smooth_tabs li:first').addClass('ui-tabs-active');

				$('ul.smooth_tabs li a').on("click", function(){
				   $('ul.smooth_tabs').find('li').removeClass('ui-tabs-active');
				   $(this).parent('li').addClass("ui-tabs-active");
				  
				   var x = $(this).attr('href');
				   $(".smooth_item").removeClass('current_catalog_item');
				   $(".tabs_content ").children('h3').removeClass('current_catalog_item');
				   $(x).addClass('current_catalog_item');
				});
			}

        });

		/* ---------------------------------------------------- */
        /*	Newsletter											*/
        /* ---------------------------------------------------- */

	    var subscribe = $('[id^="newsletter"]');
	      subscribe.append('<div class="message-container-subscribe"></div>');
	      var message = $('.message-container-subscribe'),text;

	      subscribe.on('submit',function(e){
	        var self = $(this);
	        
	        if(self.find('input[type="email"]').val() == ''){
	          text = "Please enter your e-mail!";
	          message.html('<div class="alert-box warning"><p>'+text+'</p></div>')
	            .slideDown()
	            .delay(4000)
	            .slideUp(function(){
	              $(this).html("");
	            });

	        }else{
	          self.find('span.error').hide();
	          $.ajax({
	            type: "POST",
	            url: "bat/newsletter.php",
	            data: self.serialize(), 
	            success: function(data){
	              if(data == '1'){
	                text = "Your email has been sent successfully!";
	                message.html('<div class="alert-box success"><p>'+text+'</p></div>')
	                  .slideDown()
	                  .delay(4000)
	                  .slideUp(function(){
	                    $(this).html("");
	                  })
	                  .prevAll('input[type="email"]').val("");
	              }else{
	                text = "Invalid email address!";
	                message.html('<div class="alert-box error"></i><p>'+text+'</p></div>')
	                  .slideDown()
	                  .delay(4000)
	                  .slideUp(function(){
	                    $(this).html("");
	                  });
	              }
	            }
	          });
	        }
	        e.preventDefault();
	    });

		/* ---------------------------------------------------- */
        /*	Loader												*/
        /* ---------------------------------------------------- */

		$("body").queryLoader2({
	        backgroundColor: '#fff',
	        barColor : '#f05a21',
	        barHeight: 4,
	        deepSearch:true,
	        minimumTime:1000,
	        onComplete: function(){
	        	$(".loader").fadeOut('200');
	        }
      	});

		/* ---------------------------------------------------- */
        /*	Sticky menu											*/
        /* ---------------------------------------------------- */

		$('body').Temp({
			sticky: true
		});

		
		/* ---------------------------------------------------- */
        /*	Fancybox											*/
        /* ---------------------------------------------------- */

        if($('.portfolio-holder').length){

        	if($.fancybox){

	        	$.fancybox.defaults.beforeShow = function () {

					var className = '';

			        if (this.title) {
			            // New line
			            this.title += '<br />';
			            this.title += '<div class="fancybox-share-buttons">';

			        }
			        else{
			        	this.title += '<div class="fancybox-share-buttons only">';
			        }			        

	    			this.title += '<a href="https://twitter.com/share" class="twitter-share-button" data-count="none" data-url="' + this.href + '">Tweet</a> ';

	        		// Add FaceBook like button
	    			this.title += '<iframe src="//www.facebook.com/plugins/like.php?href=http://fancyapps.com/fancybox/demo/1_b.jpg&amp;layout=button_count&amp;show_faces=true&amp;width=500&amp;action=like&amp;font&amp;colorscheme=light&amp;height=23" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:110px; height:23px;" allowtransparency="true"></iframe>';

	    			this.title += '</div>';

				};

				$.fancybox.defaults.afterShow = function(){
					// Render tweet button
					twttr.widgets.load();
				};

				$.fancybox.defaults.helpers.title = {
					type: 'inside'
				}

	        }

	        if($.fancybox){

				var $fancyBox = $('.fancybox');

				$.fancybox.defaults.padding = 0;
				$.fancybox.defaults.wrapCSS = 'custom-lightbox';

				$.fancybox.defaults.helpers.thumbs = {
					width: 80,
					height: 80
				}

				if($fancyBox.length){
					$fancyBox.fancybox();
				}

				var fancyboxMedia = $('.fancybox-media');

				if(fancyboxMedia.length){

					fancyboxMedia.fancybox({
						openEffect  : 'none',
						closeEffect : 'none',
						helpers : {
							media : {}
						}
					});

				}

			}

        }

		/* ---------------------------------------------------- */
        /*	Price Scale										    */
        /* ---------------------------------------------------- */

		var slider;
		if($('#price').length){
			slider = $('#price').slider({ 
		 		animate: true,
				range: true,
				values: [ 1, 99],
				min: 0,
				max: 100,
				slide : function(event ,ui){
					$('.range-values').find('.first-limit').val('$' + ui.values[0] + ',000');
					$('.range-values').find('.last-limit').val('$' + ui.values[1] + ',000');
				}
			});
		}
		

		/* ---------------------------------------------------- */
        /*	Accordion & Toggle									*/
        /* ---------------------------------------------------- */

		var aItem = $('.accordion:not(.toggle) .accordion-item'),
			link = aItem.find('.a-title'),
			$label = aItem.find('label'),
			aToggleItem = $('.accordion.toggle .accordion-item'),
			tLink = aToggleItem.find('.a-title');

			aItem.add(aToggleItem).children('.a-title').not('.active').next().hide();

		function triggerAccordeon($item) {
			$item
			.addClass('active')
			.next().stop().slideDown()
			.parent().siblings()
			.children('.a-title')
			.removeClass('active')
			.next().stop().slideUp();
		}


		if ($label.length) {
			$label.on('click',function(){
				triggerAccordeon($(this).closest('.a-title'))
			});
		} else {
			link.on('click',function(){
				triggerAccordeon($(this))
			});
		}

		tLink.on('click',function(){
			$(this).toggleClass('active')
			.next().stop().slideToggle();

		});

		/* ---------------------------------------------------- */
        /*	Isotope												*/
        /* ---------------------------------------------------- */

		$( window ).on('load', function() {

		  	var $container = $('.isotope');
		    // filter buttons
		    $('#filters button').on('click', function(){
		    	var $this = $(this);
		        // don't proceed if already selected
		        if ( !$this.hasClass('is-checked') ) {
		          $this.parents('#options').find('.is-checked').removeClass('is-checked');
		          $this.addClass('is-checked');
		        }
				var selector = $this.attr('data-filter');
				$container.isotope({  itemSelector: '.item', filter: selector, isOriginLeft: false });
				return false;
		    });

		    $.mad_core.isotope();
		     
		});

		/* ---------------------------------------------------- */
        /*	Quantity											*/
        /* ---------------------------------------------------- */

		var q = $('.quantity');

		q.each(function(){
			var $this = $(this),
				button = $this.children('button'),
				input = $this.children('input[type="text"]'),
				val = +input.val();

			button.on('click',function(){
				if($(this).hasClass('qty-minus')){
					if(val === 1) return false;
					input.val(--val);
				}
				else{
					input.val(++val);
				}
			});
		});

		/* ---------------------------------------------------- */
        /*	Contact Form										*/
        /* ---------------------------------------------------- */

		if ($('#contact-form').length){

			var cf = $('#contact-form');
			cf.append('<div class="message-container"></div>');

			cf.on("submit",function(event){

				var self = $(this),text;

				var request = $.ajax({
					url:"bat/mail.php",
					type : "post",
					data : self.serialize()
				});

				request.then(function(data){
					if(data == "1"){

						text = "Your message has been sent successfully!";

						cf.find('input:not([type="submit"]),textarea').val('');

						$('.message-container').html('<div class="alert-box success"><i class="icon-smile"></i><p>'+text+'</p></div>')
							.delay(150)
							.slideDown(300)
							.delay(4000)
							.slideUp(300,function(){
								$(this).html("");
							});

					}
					else{
						if(cf.find('textarea').val().length < 20){
							text = "Message must contain at least 20 characters!"
						}
						if(cf.find('input').val() == ""){
							text = "All required fields must be filled!";
						}
						$('.message-container').html('<div class="alert-box error"><i class="icon-warning"></i><p>'+text+'</p></div>')
							.delay(150)
							.slideDown(300)
							.delay(4000)
							.slideUp(300,function(){
								$(this).html("");
							});
					}
				},function(){
					$('.message-container').html('<div class="alert-box error"><i class="icon-warning"></i><p>Connection to server failed!</p></div>')
							.delay(150)
							.slideDown(300)
							.delay(4000)
							.slideUp(300,function(){
								$(this).html("");
							});
				});

				event.preventDefault();

			});

		}

		/* ---------------------------------------------------- */
		/*	Animate a regular anchor navigation					*/
		/* ---------------------------------------------------- */

	    if ($('a.animated').length) {

	    	$('body').localScroll({
	           hash: true,
	           filter: '.animated',
	           onBefore: function(){
                 this.offset = 0;
               }
	        });

	    }

		/* ---------------------------------------------------- */
		/*	Google Maps											*/
		/* ---------------------------------------------------- */

		if ($('#googleMap').length) {

			$(document).ready(function() {

				function loadMap() {
				  	var mapProp = {
					    center: {lat: 51.503454, lng: -0.124755},
					    zoom:15,
					    mapTypeId:google.maps.MapTypeId.ROADMAP

					};

					var map = document.getElementById('googleMap');

					if(map !== null){

				    	var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

					}
		            
		            setMarkers(map);

				}
				var marks = [
				  ['first', 51.503454,-0.111562]
				];

	            function setMarkers(map) {

					for (var i = 0; i < marks.length; i++) {
						var mark = marks[i];
						var marker = new google.maps.Marker({
						  position: {lat: mark[1], lng: mark[2]},
						  map: map,
						  title: mark[0],
						  zIndex: mark[3]
						});
					}
				}
				google.maps.event.addDomListener(window, 'load', loadMap);

			});
			
		}

		/* ---------------------------------------------------- */
		/*	Sticky footer										*/
		/* ---------------------------------------------------- */

		$(window).on("load resize",function(){

			var BoxeeBox = $('#footer'); /* cache the selector */

		    if ($(window).width() > 1281) {

		        $('#content').css({ 'margin-bottom': BoxeeBox.outerHeight() });

		    } else{

		    	$('#content').css({ "margin-bottom": "0" });

		    }

		});

		/* ---------------------------------------------------- */
		/*	Countdown											*/
		/* ---------------------------------------------------- */

		$('.countdown').each(function(){
			var $this = $(this),
				endDate = $this.data(),
				until = new Date(
					endDate.year,
					endDate.month || 0,
					endDate.day || 1,
					endDate.hours || 0,
					endDate.minutes || 0,
					endDate.seconds || 0
				);
			// initialize
			$this.countdown({
				until : until,
				format : 'dHMS',
				labels : ['years', 'month', 'weeks', 'days', 'hours', 'min', 'sec']
			});
		});
		
		$('.entry-share').click(function(){
			var url = this.getAttribute('url');
			var text = this.getAttribute('text');
			var vk = 'https://vk.com/share.php?url='+url;
			var whatsapp = 'https://api.whatsapp.com/send?text='+url;
			var fb = 'www.facebook.com/dialog/share?app_id=324966041266385&href='+url+'&name='+text+'&amp;display=popup&link=#&redirect_uri=#close_window';
			var tw = 'https://twitter.com/intent/tweet?url='+url+'&text='+text;
			var tg = 'tg://msg_url?url='+url+'&text='+text;
			$('#share-link-tg').attr( "href", tg );
			$('#share-link-vk').attr( "href", vk );
			$('#share-link-whatsapp').attr( "href", whatsapp );
			$('#share-link-fb').attr( "href", fb );
			$('#share-link-tw').attr( "href", tw );
			$('.social-share').slideToggle( "slow", function() {
    // Animation complete.
  			});
		});

		$('.social-share-close').click(function() {
			$('.social-share').slideUp("slow", function() {
    // Animation complete.
  			});
		});
	});
	
})(jQuery);