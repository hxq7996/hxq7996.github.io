menu_active()
function menu_active() {
  if (document.URL.lastIndexOf('lyear')===-1) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    
  }
  if (document.URL.lastIndexOf('lyear_pages_doc') > 0) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    obj = document.getElementById('menu_0_0');
    obj.className += ' active'; // 注意前面加空格，防止两个属性挨一起
  }
  if (document.URL.lastIndexOf('lyear_pages_gd_doc') > 0) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    obj = document.getElementById('menu_0_1');
    obj.className += ' active'; // 注意前面加空格，防止两个属性挨一起
  }
  if (document.URL.lastIndexOf('lyear_pages_user_doc') > 0) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    obj = document.getElementById('menu_0_2');
    obj.className += ' active'; // 注意前面加空格，防止两个属性挨一起
  }
  if (document.URL.lastIndexOf('lyear_pages_gdc_doc') > 0) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    obj = document.getElementById('menu_0_3');
    obj.className += ' active'; // 注意前面加空格，防止两个属性挨一起
  }
  if (document.URL.lastIndexOf('lyear_pages_ip_doc') > 0) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    obj = document.getElementById('menu_0_4');
    obj.className += ' active'; // 注意前面加空格，防止两个属性挨一起
  }
  if (document.URL.lastIndexOf('lyear_pages_rabc') > 0) {
    var obj = document.getElementById('menu_0');
    obj.className += ' active open'; // 注意前面加空格，防止两个属性挨一起
    obj = document.getElementById('menu_0_5');
    obj.className += ' active'; // 注意前面加空格，防止两个属性挨一起
  }
}