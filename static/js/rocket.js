
//<![CDATA[
jQuery(window).scroll(function(){jQuery(window).scrollTop()<50?jQuery("#rocketmeluncur").slideUp(500):jQuery("#rocketmeluncur").slideDown(500);var e=jQuery("#ft")[0]?jQuery("#ft")[0]:jQuery(document.body)[0],t=$("rocketmeluncur"),n=(parseInt(document.documentElement.clientHeight),parseInt(document.body.getBoundingClientRect().top),parseInt(e.clientWidth)),r=t.clientWidth;if(1e3>n){var l=parseInt(fetchOffset(e).left);l=r>l?2*l-r:l,t.style.left=n+l+"px"}else t.style.left="auto",t.style.right="10px"}),jQuery("#rocketmeluncur").click(function(){jQuery("html, body").animate({scrollTop:"0px",display:"none"},{duration:600,easing:"linear"});var e=this;this.className+=" launchrocket",setTimeout(function(){e.className="showrocket"},800)});
//]]>
