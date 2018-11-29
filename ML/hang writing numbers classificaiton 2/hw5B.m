xtrain= csvread('X_train.csv');%讀取檔案
ttrain = csvread('T_train.csv');
xtest = csvread('X_test.csv');
ttest = csvread('T_test.csv');


M=2; %hidden layer十層
dim=784;
w1=zeros([M dim]);
random1=2*rand(M,dim)-1;
for ww=1:M
    for j=1:dim
       w1(ww,j)=0.001*random1(ww,j);
    end
end 
w2=zeros([M 1])+0.0001;
tag=5;
w3=zeros([tag M]);
random2=2*rand(M,tag)-1;
for ww=1:M
    for tj=1:tag
        w3(tj,ww)=0.001*random2(ww,tj);
    end
end 
w4=zeros([tag 1])+0.001;
aj=zeros([M 1]);
zj=zeros([M 1]);
ak=zeros([tag 1]);
yk=zeros([tag 1]);
parth=zeros([M 1]); %h(zj)的微分

target=zeros([5 length(xtrain)]);
learnrate1=0.001;
learnrate2=0.001;
learnrate4=0.001;
learnrate3=0.001;

 for j=1:1000
      target(1,j)=1;
      target(2,j+1000)=1;
      target(3,j+2000)=1;      
      target(4,j+3000)=1;  
      target(5,j+4000)=1;  
  end     
xtrainT=transpose(xtrain);


for time=1:1000
for i=1:length(xtrain)
    aj=w1*xtrainT(:,i)+w2; 
    for j=1:M
    zj(j,:)=1/(1+exp(-aj(j,:)));
    end
     ak=w3*zj+w4;
     a4=max([ak(1,:),ak(2,:),ak(3,:),ak(4,:),ak(5,:)]);
     if a4==NaN
         break 
     end   
     ak(1,:)=ak(1,:)-a4;
     ak(2,:)=ak(2,:)-a4;
     ak(3,:)=ak(3,:)-a4;
     ak(4,:)=ak(4,:)-a4;
     ak(5,:)=ak(5,:)-a4;
     SS=exp(ak(1,:))+exp(ak(2,:))+exp(ak(3,:))+exp(ak(4,:))+exp(ak(5,:));
     yk(1,:)=exp(ak(1,:))/(SS);
     yk(2,:)=exp(ak(2,:))/(SS);
     yk(3,:)=exp(ak(3,:))/(SS);
     yk(4,:)=exp(ak(4,:))/(SS);
     yk(5,:)=exp(ak(5,:))/(SS);
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

XX=zeros([M length(xtrain)]);
for i=1:length(xtrain)
  XX(:,i)=w1*xtrainT(:,i)+w2;
end
XXT=transpose(XX);
%b = TreeBagger(100,xtrainpca,ttrain,'InBagFraction',0.5,'OOBPred','on','Method','classification','minleaf',1000)
a=zeros([100 1]);
%for num=1:100
    %k=num/100;
b = TreeBagger(100,XXT,ttrain,'InBagFraction',1,'OOBPred','on','Method','classification','minleaf',100);
%view(b.Trees{1},'Mode','graph')
xtestT=transpose(xtest);

YY=zeros([M length(xtest)]);
for i=1:length(xtest)
    YY(:,i)=w1*xtestT(:,i)+w2;
end
YYT=transpose(YY);
[K] = predict(b, YYT);
Y=str2num(char(K));
error=0;
for i=1:500
    if Y(i)~=1
    error=error+1;
    end
    
    if Y(i+500)~=2
    error=error+1;
    end
   
    if Y(i+1000) ~= 3
    error=error+1;
    end
    
    if Y(i+1500)~=4
    error=error+1;
    end
    
    if Y(i+2000)~=5
    error=error+1;
    end
end     
error

%a(num,:)=error;
%end 
%csvwrite('a.csv',a)
%繪decision region

figure(1)

PCAX=XXT;
[xi,yi] = meshgrid([min(XXT(:,1)):1:max(XXT(:,1))],[min(XXT(:,2)):1:max(XXT(:,2))]);
dd = [xi(:),yi(:)];
[A] = predict(b,dd); 
predicted_label=str2num(char(A));

redcolor = [1 0.8 0.8];
bluecolor = [0.8 0.8 1];
greencolor = [0.8 1 0.8];
ccolor = [0.5 1 0.3];
dcolor = [0.2 0.6 0.3];
pos = find(predicted_label==1);
h1 = plot(dd(pos,1),dd(pos,2),'s','color',redcolor,'MarkerSize',5,'MarkerEdgeColor',redcolor,'MarkerFaceColor',redcolor);
hold on;
pos = find(predicted_label==2);
h2 = plot(dd(pos,1),dd(pos,2),'s','color',bluecolor,'MarkerSize',5,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',bluecolor);
hold on 
pos = find(predicted_label==3);
h3 = plot(dd(pos,1),dd(pos,2),'s','color',greencolor,'MarkerSize',5,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',greencolor);
hold on
pos = find(predicted_label==4);
h4 = plot(dd(pos,1),dd(pos,2),'s','color',ccolor,'MarkerSize',5,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',ccolor);
hold on 
pos = find(predicted_label==5);
h5 = plot(dd(pos,1),dd(pos,2),'s','color',dcolor,'MarkerSize',5,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',dcolor);
hold on 
uistack(h1, 'bottom');
uistack(h2, 'bottom');
uistack(h3, 'bottom');
uistack(h4, 'bottom');
uistack(h5, 'bottom');
plot(PCAX(1:1000,1),PCAX(1:1000,2),'. r');
hold on
plot(PCAX(1001:2000,1),PCAX(1001:2000,2),'. g');
hold on
plot(PCAX(2001:3000,1),PCAX(2001:3000,2),'. b');
hold on
plot(PCAX(3001:4000,1),PCAX(3001:4000,2),'. m');
hold on
plot(PCAX(4001:5000,1),PCAX(4001:5000,2),'. y');
axis([min(XXT(:,1)),max(XXT(:,1)),min(XXT(:,2)),max(XXT(:,2))])
hold on

