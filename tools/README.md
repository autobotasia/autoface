# autoface-tool

## Launch webpage
python manage.py migrate (*to save changes*)

python manage.py runserver

## Web Tools

Image Model:
  - img_url: địa chỉ tương đối của ảnh trong thư mục static
  - img_tag: nhãn của ảnh
  - visited: ảnh trong thư mục đã được duyệt qua hay chưa. Dùng để  lọc những ảnh đã duyệt rồi sẽ không được duyệt trong lần chạy lại tool.

tag_list:
  - Lưu danh sách các nhãn

*Temp Image Folder location: settings.py -> TEMP_IMG*
url cho database crud:
  - <host>/crud/<str:action>:
  - action == "reset-visited-value": thiết lập biến visited của tất cả các img object về  
  - action == "delete-all": xóa toàn bộ record trong database
  - action == "save-image-data-to-database" = lưu dữ liệu ảnh trong thư mục "Temp Image Folder location: settings.py -> TEMP_IMG" vào db
  - action == "delete":
  + <host>/crud/delete/<int:img_pk>: xóa img object có pk bằng img pk

## Web Management
