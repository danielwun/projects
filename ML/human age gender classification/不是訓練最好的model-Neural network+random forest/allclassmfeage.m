%neuralnetwork降維加上利用randforest去分類
%分男性和女性
%讀取調整亮度後的資料
byoungm= csvread('youngms.csv');
byoungf= csvread('youngfs.csv');
badultm= csvread('adultms.csv');
badultf= csvread('adultfs.csv');
bchildm= csvread('childms.csv');
bchildf= csvread('childfs.csv');
belderm= csvread('elderms.csv');
belderf= csvread('elderfs.csv');
%去製造neural network所需要的target
[n00 d]=size(bchildm);
[n04 d]=size(bchildf);

[n01 d]=size(byoungm);
[n05 d]=size(byoungf);


[n02 d]=size(badultm);
[n06 d]=size(badultf);

[n03 d]=size(belderm);
[n07 d]=size(belderf);
%做validation 
numval=50;
n0=n00-numval;
n1=n01-numval;
n2=n02-numval;
n3=n03-numval;
n4=n04-numval;
n5=n05-numval;
n6=n06-numval;
n7=n07-numval;

ntarget=n0+n1+n2+n3+n4+n5+n6+n7;
target=zeros([2 ntarget]);
ttrain=zeros([ntarget 1]);
%{
for i=1:n0
    target(1,i)=1;
    ttrain(i)=0;
end
for i=n0+1:n0+n1
    target(2,i)=1;
    ttrain(i)=1;
end
for i=n0+n1+1:n0+n1+n2
    target(3,i)=1;
    ttrain(i)=2;
end
for i=n0+n1+n2+1:n0+n1+n2+n3
    target(4,i)=1;
    ttrain(i)=3;
end
for i=n0+n1+n2+n3+1:n0+n1+n2+n3+n4
    target(5,i)=1;
    ttrain(i)=4;
end
for i=n0+n1+n2+n3+n4+1:n0+n1+n2+n3+n4+n5
    target(6,i)=1;
    ttrain(i)=5;
end
for i=n0+n1+n2+n3+n4+n5+1:n0+n1+n2+n3+n4+n5+n6
    target(7,i)=1;
    ttrain(i)=6;
end
for i=n0+n1+n2+n3+n4+n5+n6+1:ntarget
    target(8,i)=1;
    ttrain(i)=7;
end
%}
%男性和女性目標
for i=1:n0+n1+n2+n3
    target(1,i)=1;
    ttrain(i)=8;
end
for i=n0+n1+n2+n3+1:ntarget
    target(2,i)=1;
    ttrain(i)=9;
end

xtrain=[bchildm(1:n0,:);byoungm(1:n1,:);badultm(1:n2,:);belderm(1:n3,:);bchildf(1:n4,:);byoungf(1:n5,:);badultf(1:n6,:);belderf(1:n7,:)];
xtrainT=transpose(xtrain);
%neural network
xtrain=xtrain./255;
M=10; %hidden layer十層
dim=d;
w1=zeros([M dim]);
random1=(2*rand(M,dim)-1)./dim;
for ww=1:M
    for j=1:dim
       w1(ww,j)=random1(ww,j);
    end
end 
w2=(2*rand(M,1)-1).*0.01;
%zeros([M 1])+0.001;
tag=2;
w3=zeros([tag M]);
random2=(2*rand(M,tag)-1)./dim;
for ww=1:M
    for tj=1:tag
        w3(tj,ww)=random2(ww,tj);
    end
end 
w4=(2*rand(tag,1)-1).*0.01;
%zeros([tag 1])+0.001;
aj=zeros([M 1]);
zj=zeros([M 1]);
ak=zeros([tag 1]);
yk=zeros([tag 1]);
parth=zeros([M 1]); %h(zj)的微分

learnrate1=0.005;
learnrate2=0.005;
learnrate4=0.005;
learnrate3=0.005;
JII=size(xtrain)
for time=1:100
for i=1:JII(1)
    aj=w1*xtrainT(:,i)+w2; 
    for j=1:M
    zj(j,:)=1/(1+exp(-aj(j,:)));
    end
     ak=w3*zj+w4;
     a4=max([ak(1,:),ak(2,:)]);
     if a4==NaN
         break 
     end   
     ak(1,:)=ak(1,:)-a4;
     ak(2,:)=ak(2,:)-a4;
   
     SS=exp(ak(1,:))+exp(ak(2,:));
     yk(1,:)=exp(ak(1,:))/(SS);
     yk(2,:)=exp(ak(2,:))/(SS);
     
     deltak=yk-target(:,i);
     grid2=deltak*transpose(zj);
     for j=1:M
     parth(j,:)=zj(j,:)*(1-zj(j,:)); 
     end   
     sig=transpose(w3)*deltak;
     for j=1:M
     deltaj(j,:)=parth(j,:)*sig(j,1); 
     end  
     grid1=deltaj*transpose(xtrainT(:,i));
     w3=w3-learnrate3*grid2;
     w1=w1-learnrate1*grid1;
     
     gridcon4=deltak;
     gridcon2=(transpose(w4)*deltak)*parth;
     w2=w2-learnrate2*gridcon2;
     w4=w4-learnrate4*gridcon4;
     
     end    
time
end
%neural network error
%{
XXn=zeros([M length(xtrain)]);
for i=1:length(xtrain)
  XXn(:,i)=w1*xtrainT(:,i)+w2;
  
end
XXnT=transpose(XXn);
%}


%randforest

XX=zeros([M JII(1)]);

for i=1:JII(1)
  XX(:,i)=w1*xtrainT(:,i)+w2;
end
XXT=transpose(XX);
b = TreeBagger(1000,XXT,ttrain,'InBagFraction',1,'OOBPred','on','Method','classification','minleaf',100);


xtest=[bchildm((1+n0):n00,:);byoungm((1+n1):n01,:);badultm((1+n2):n02,:);belderm((1+n3):n03,:);bchildf((1+n4):n04,:);byoungf((1+n5):n05,:);badultf((1+n6):n06,:);belderf((1+n7):n07,:)];
XXtest=zeros([M length(xtest)]);
xtestT=transpose(xtest);
xtestTmat=size(xtestT);    
w2ma=zeros([1 xtestTmat(2)])+1;
XXtest=w1*xtestT+w2*(w2ma);

XXTtest=transpose(XXtest);


[K] = predict(b, XXTtest);
Y=str2num(char(K));
error=0;


 %{
for i=1:n0
    if Y(i)~=0
    error=error+1;
    end
end
for i=n0+1:n0+n1
    if Y(i)~=1
    error=error+1;
    end
end
for i=n0+n1+1:n0+n1+n2
     if Y(i)~=2
    error=error+1;
    end
end
for i=n0+n1+n2+1:n0+n1+n2+n3
     if Y(i)~=3
    error=error+1;
    end
end
for i=n0+n1+n2+n3+1:n0+n1+n2+n3+n4
    if Y(i)~=4
    error=error+1;
    end
end
for i=n0+n1+n2+n3+n4+1:n0+n1+n2+n3+n4+n5
     if Y(i)~=5
    error=error+1;
    end
end
for i=n0+n1+n2+n3+n4+n5+1:n0+n1+n2+n3+n4+n5+n6
     if Y(i)~=6
    error=error+1;
    end
end
for i=n0+n1+n2+n3+n4+n5+n6+1:ntarget
     if Y(i)~=7
    error=error+1;
    end
end
%}
%{
for i=1:numval
    if Y(i)~=0
    error=error+1;
    end
end
for i=numval+1:numval*2
    if Y(i)~=1
    error=error+1;
    end
end
for i=numval*2+1:numval*3
     if Y(i)~=2
    error=error+1;
    end
end
for i=numval*3+1:numval*4
     if Y(i)~=3
    error=error+1;
    end
end
for i=numval*4+1:numval*5
    if Y(i)~=4
    error=error+1;
    end
end
for i=numval*5+1:numval*6
     if Y(i)~=5
    error=error+1;
    end
end
for i=numval*6+1:numval*7
     if Y(i)~=6
    error=error+1;
    end
end
for i=numval*7+1:numval*8
     if Y(i)~=7
    error=error+1;
    end
end
%}
for i=1:numval*4
    if Y(i)~=8
    error=error+1;
    end
end
error
for i=numval*4+1:numval*8
    if Y(i)~=9
    error=error+1;
    end
end

error

%年紀分類


target2=zeros([4 ntarget]);
ttrain=zeros([ntarget 1]);

for i=1:n0
    target(1,i)=1;
    ttrain(i)=10;
end
for i=n0+1:n0+n1
    target(2,i)=1;
    ttrain(i)=11;
end
for i=n0+n1+1:n0+n1+n2
    target(3,i)=1;
    ttrain(i)=12;
end
for i=n0+n1+n2+1:n0+n1+n2+n3
    target(4,i)=1;
    ttrain(i)=13;
end
for i=n0+n1+n2+n3+1:n0+n1+n2+n3+n4
    target(1,i)=1;
    ttrain(i)=10;
end
for i=n0+n1+n2+n3+n4+1:n0+n1+n2+n3+n4+n5
    target(2,i)=1;
    ttrain(i)=11;
end
for i=n0+n1+n2+n3+n4+n5+1:n0+n1+n2+n3+n4+n5+n6
    target(3,i)=1;
    ttrain(i)=12;
end
for i=n0+n1+n2+n3+n4+n5+n6+1:ntarget
    target(4,i)=1;
    ttrain(i)=13;
end


%neural network
xtrain=xtrain./255;
M=10; %hidden layer十層
dim=d;
w1=zeros([M dim]);
random1=(2*rand(M,dim)-1)./dim;
for ww=1:M
    for j=1:dim
       w1(ww,j)=random1(ww,j);
    end
end 
w2=(2*rand(M,1)-1).*0.01;
%zeros([M 1])+0.001;
tag=4;
w3=zeros([tag M]);
random2=(2*rand(M,tag)-1)./dim;
for ww=1:M
    for tj=1:tag
        w3(tj,ww)=random2(ww,tj);
    end
end 
w4=(2*rand(tag,1)-1).*0.01;
%zeros([tag 1])+0.001;
aj=zeros([M 1]);
zj=zeros([M 1]);
ak=zeros([tag 1]);
yk=zeros([tag 1]);
parth=zeros([M 1]); %h(zj)的微分

learnrate1=0.005;
learnrate2=0.005;
learnrate4=0.005;
learnrate3=0.005;
JII=size(xtrain)
for time2=1:100
for i=1:JII(1)
    aj=w1*xtrainT(:,i)+w2; 
    for j=1:M
    zj(j,:)=1/(1+exp(-aj(j,:)));
    end
     ak=w3*zj+w4;
     a4=max([ak(1,:),ak(2,:),ak(3,:),ak(4,:)]);
     if a4==NaN
         break 
     end   
     ak(1,:)=ak(1,:)-a4;
     ak(2,:)=ak(2,:)-a4;
     ak(3,:)=ak(3,:)-a4;
     ak(4,:)=ak(4,:)-a4;
     SS=exp(ak(1,:))+exp(ak(2,:))+exp(ak(3,:))+exp(ak(4,:));
     yk(1,:)=exp(ak(1,:))/(SS);
     yk(2,:)=exp(ak(2,:))/(SS);
     yk(3,:)=exp(ak(3,:))/(SS);
     yk(4,:)=exp(ak(4,:))/(SS);
     deltak=yk-target(:,i);
     grid2=deltak*transpose(zj);
     for j=1:M
     parth(j,:)=zj(j,:)*(1-zj(j,:)); 
     end   
     sig=transpose(w3)*deltak;
     for j=1:M
     deltaj(j,:)=parth(j,:)*sig(j,1); 
     end  
     grid1=deltaj*transpose(xtrainT(:,i));
     w3=w3-learnrate3*grid2;
     w1=w1-learnrate1*grid1;
     
     gridcon4=deltak;
     gridcon2=(transpose(w4)*deltak)*parth;
     w2=w2-learnrate2*gridcon2;
     w4=w4-learnrate4*gridcon4;
     
     end    
time2
end

XX=zeros([M JII(1)]);

for i=1:JII(1)
  XX(:,i)=w1*xtrainT(:,i)+w2;
end

XXT=transpose(XX);
b2 = TreeBagger(1000,XXT,ttrain,'InBagFraction',1,'OOBPred','on','Method','classification','minleaf',100);


xtest=[bchildm((1+n0):n00,:);byoungm((1+n1):n01,:);badultm((1+n2):n02,:);belderm((1+n3):n03,:);bchildf((1+n4):n04,:);byoungf((1+n5):n05,:);badultf((1+n6):n06,:);belderf((1+n7):n07,:)];
XXtest=zeros([M length(xtest)]);
xtestT=transpose(xtest);
xtestTmat=size(xtestT);    
w2ma=zeros([1 xtestTmat(2)])+1;
XXtest=w1*xtestT+w2*(w2ma);
XXTtest=transpose(XXtest);
[K2] = predict(b2, XXTtest);
Y2=str2num(char(K2));
error2=0;
%{
for i=1:n0
    if Y2(i)~=10
    error2=error2+1;
    end
end
for i=n0+1:n0+n1
    if Y2(i)~=11
    error2=error2+1;
    end
end
for i=n0+n1+1:n0+n1+n2
     if Y2(i)~=12
    error2=error2+1;
    end
end
for i=n0+n1+n2+1:n0+n1+n2+n3
     if Y2(i)~=13
    error2=error2+1;
    end
end
for i=n0+n1+n2+n3+1:n0+n1+n2+n3+n4
    if Y2(i)~=10
    error2=error2+1;
    end
end
for i=n0+n1+n2+n3+n4+1:n0+n1+n2+n3+n4+n5
     if Y2(i)~=11
    error2=error2+1;
    end
end
for i=n0+n1+n2+n3+n4+n5+1:n0+n1+n2+n3+n4+n5+n6
     if Y2(i)~=12
    error2=error2+1;
    end
end
for i=n0+n1+n2+n3+n4+n5+n6+1:ntarget
     if Y2(i)~=13
    error2=error2+1;
    end
end
error2
%}




%%%%
for i=1:numval
    if Y2(i)~=10
    error2=error2+1;
    end
end
for i=numval+1:2*numval
    if Y2(i)~=11
    error2=error2+1;
    end
end
for i=2*numval+1:3*numval
     if Y2(i)~=12
    error2=error2+1;
    end
end
for i=3*numval+1:4*numval
     if Y2(i)~=13
    error2=error2+1;
    end
end
for i=4*numval+1:5*numval
    if Y2(i)~=10
    error2=error2+1;
    end
end
for i=5*numval+1:6*numval
     if Y2(i)~=11
    error2=error2+1;
    end
end
for i=6*numval+1:7*numval
     if Y2(i)~=12
    error2=error2+1;
    end
end
for i=7*numval+1:8*numval
     if Y2(i)~=13
    error2=error2+1;
    end
end
error2

finaltarget=zeros([8*numval 1]);
for i=1:8*numval
      if Y(i)==8
        if Y2(i)==10
              finaltarget(i)=0;
        end 
        if Y2(i)==11
             finaltarget(i)=1;
        end
        if Y2(i)==12
             finaltarget(i)=2;
        end
        if Y2(i)==13
             finaltarget(i)=3;
        end
       
      end
      if Y(i)==9
           if Y2(i)==10
              finaltarget(i)=4;
        end 
        if Y2(i)==11
             finaltarget(i)=5;
        end
        if Y2(i)==12
             finaltarget(i)=6;
        end
        if Y2(i)==13
             finaltarget(i)=7;
        end
      end
end    
 %最後總共錯誤
finallerror=0;
for i=1:numval
    if  finaltarget(i)~=0
    finallerror=finallerror+1;
    end
end
for i=1+numval:2*numval
    if  finaltarget(i)~=1
    finallerror=finallerror+1;
    end
end
for i=1+numval*2:3*numval
    if  finaltarget(i)~=2
    finallerror=finallerror+1;
    end
end
for i=1+numval*3:4*numval
    if  finaltarget(i)~=3
    finallerror=finallerror+1;
    end
end
for i=1+numval*4:5*numval
    if  finaltarget(i)~=4
    finallerror=finallerror+1;
    end
end
for i=1+numval*5:6*numval
    if  finaltarget(i)~=5
    finallerror=finallerror+1;
    end
end
for i=1+numval*6:7*numval
    if  finaltarget(i)~=6
    finallerror=finallerror+1;
    end
end
for i=1+numval*7:8*numval
    if  finaltarget(i)~=7
    finallerror=finallerror+1;
    end
end
