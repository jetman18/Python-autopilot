# Flightgear-simulation
Chương trình mô phỏng, điều khiển dẫn đường cho máy bay cánh bằng trên phần mềm bay giả lập Flightgear sử dụng python

**Chức năng cơ bản*
- Bay bám theo tọa độ thiết lập sẵn
- Bay vòng tròn Loiter
- ...

![exampl](./resource/hmm.png)

![exampl](./resource/image3.png)
# Thuật toán dẫn đường
+ Phương pháp vector tọa độ "Vector Field Guidance"
+ Tham khảo bài báo "Autonomous Waypoint-based Guidance
Methods for Small Size Unmanned Aerial
Vehicles" [https://acta.uni-obuda.hu/Stojcsics_56.pdf]
+ file 'vectorGeneration.py' sử dụng để vẽ các vector thiết lập thử các hệ số 
+ Điều khiển máy bay bám theo hướng các vector [hình 1] bay vòng tròn,  [hình 2] bay bám quỹ đạo 


   <img align="left" src="./resource/loiter.png" alt="img-name"  width="320" height="250"><img align="right" src="./resource/waypoint.png"  width="320" height="250">
   <br clear="left"/>
     
