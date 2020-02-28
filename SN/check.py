
s = [f'192.168.0.{i}' for i in range(3,101)]
s.extend(['0.0.0.0', '127.0.0.1']) # бляяяя возврат то нон

print(s)




info jquery


https://medium.com/@stasonmars/%D0%BF%D0%B5%D1%80%D0%B5%D1%85%D0%BE%D0%B4%D0%B8%D0%BC-%D1%81-jquery-%D0%BD%D0%B0-%D1%87%D0%B8%D1%81%D1%82%D1%8B%D0%B8%CC%86-javascript-e2b3c2c6ab4

https://learn.javascript.ru/mousemove-mouseover-mouseout-mouseenter-mouseleave

https://learn.javascript.ru/event-loop

https://learn.javascript.ru/settimeout-setinterval





preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_chats)])
        queryset = self.filter(pk__in=sorted_chats).order_by(preserved)


* -> insert in case list ( *args)


SELECT *
FROM theme
ORDER BY
  CASE
    WHEN id=10 THEN 0
    WHEN id=2 THEN 1
    WHEN id=1 THEN 2
  END;





 var airbrake = null;
 function startAirbrakeClient() {
 try {
 airbrake = new airbrakeJs.Client({
 projectId: 185599,
 projectKey: '7d54cb700ee05d483e2dd168401542d4'
 });
 airbrake.addFilter(function (notice) {
 notice.context.environment = 'production';
 return notice;
 });
 airbrake.addFilter(function(notice) {
 if (notice.errors[0] && notice.errors[0].message == 'Too many requests in last minute - account is rate limited') {
 return null;
 }
 return notice;
 });
 } catch(e) {
 }
 }

 document.addEventListener("DOMContentLoaded", function () {
 // PAN-48586
 startAirbrakeClient();

 var brakeLimit = 0;
 var brake = setInterval(function () {
 var placeholdersList = document.querySelectorAll("[id$='__preloader']");
 if (!placeholdersList.length) {
 clearInterval(brake);
 return;
 }
 if (brakeLimit > 2) {
 var scriptsNodeList = document.querySelectorAll("script"),
 scripts = [],
 notLoadedComponents = [];
 for (var i = 0; i < scriptsNodeList.length; i++) {
 if (scriptsNodeList[i].src) {
 scripts.push(scriptsNodeList[i].src)
 }
 }
 for (var i = 0; i < placeholdersList.length; i++) {
 var element = placeholdersList[i].parentNode;
 notLoadedComponents.push(element.getAttribute("data-react-component") || element.getAttribute("data-vue-component") || element.getAttribute("id"));
 }

 airbrake.notify({
 'error': new Error('Placeholders not replaced'),
 'context': {
 'wasOnline': navigator.onLine,
 'notLoadedComponents': notLoadedComponents,
 'scripts': scripts,
 'url': location.href
 },
 });

 clearInterval(brake);
 return;
 } else {
 brakeLimit++;
 }
 }, 2000);
 });
 