(function($) {
	
	$(document).ready(function() {
		$(".donate img, .social img").hover(
			function() { this.src = this.src.replace("_on", "_off");
		},
			function() { this.src = this.src.replace("_off", "_on");
		});
	});
	
})(jQuery);