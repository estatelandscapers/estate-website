/* Meta (Facebook) Pixel 1901484014154708 — loaded as a file so the site's CSP allows it.
   The fbq queue and PageView are set up at once; the 240 KB fbevents.js itself is fetched
   by site.js on the visitor's first interaction (or after 10 s), so it never slows the
   page load. Anything tracked before then waits in the queue and is sent when it loads. */
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];
f.elLoadPixel=function(){if(f.__elPixelIn)return;f.__elPixelIn=1;t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)};
if(f.__elTrackersGo)f.elLoadPixel()}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1901484014154708');
fbq('track', 'PageView');
