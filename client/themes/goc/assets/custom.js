;(function(){

  function removeElementsByClass(className){
    var elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
  }

  setInterval(function(){
        var isVerifiedPerson = ( window.location.href.indexOf('verified_person.cc.orgbook.canada.ca') > -1 ) ? true : false;

        if ( isVerifiedPerson )
        {
          removeElementsByClass('vp_omit');
        }
  }, 500);


})();
