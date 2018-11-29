[label, inst] = libsvmread('PCAX.txt');

%-s 0 -t 0  


%[bestCVaccuracy,bestc,bestg]=SVMcg(label,inst,-20,20,-20,20);
%cmd = ['-s 0 -t 0','-c ',num2str(bestc),' -g ',num2str(bestg)]
%model = svmtrain(label, inst, cmd);

model = svmtrain(label, inst,'-s 1 -t 1 -d 3  -n 0.06 -g 1');

[label2, inst2] = libsvmread('xtestpca.txt');
[predict_label, accuracy, dec_values] = svmpredict(label2,inst2, model);

A = csvread('X_train.csv');
[eigenVectors,score,eigenValues,tsquare]= princomp(A);
transMatrix = eigenVectors(:,1:2);  %取前兩大
Asum=sum(A)/4999; 
AT=transpose(A);
B=zeros([784 5000]);         
for i=1:784
B(i,:)=AT(i,:)-Asum(i);
end
PCAX=transpose(B)*transMatrix;
%}

%[predict_labeltrain] = svmpredict(label,inst, model);

sv = full(model.SVs);

%
figure
%now plot decision area
redcolor = [1 0.8 0.8];
bluecolor = [0.8 0.8 1];
greencolor = [0.8 1 0.8];
ccolor = [0.5 1 0.3];
dcolor = [0.2 0.6 0.3];

[xi,yi] = meshgrid([min(PCAX(:,1)):0.1:max(PCAX(:,1))],[min(PCAX(:,2)):0.1:max(PCAX(:,2))]);
dd = [xi(:),yi(:)];
[ddlabel, ddinst] = libsvmread('ddfin.txt');
tic;[predicted_label, accuracy, decision_values] = svmpredict(ddlabel, ddinst, model);toc
hold on;
pos = find(predicted_label==1);
h1 = plot(dd(pos,1),dd(pos,2),'s','color',redcolor,'MarkerSize',10,'MarkerEdgeColor',redcolor,'MarkerFaceColor',redcolor);
hold on;
pos = find(predicted_label==2);
h2 = plot(dd(pos,1),dd(pos,2),'s','color',bluecolor,'MarkerSize',10,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',bluecolor);
hold on 
pos = find(predicted_label==3);
h3 = plot(dd(pos,1),dd(pos,2),'s','color',greencolor,'MarkerSize',10,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',greencolor);
hold on
pos = find(predicted_label==4);
h4 = plot(dd(pos,1),dd(pos,2),'s','color',ccolor,'MarkerSize',10,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',ccolor);
hold on 
pos = find(predicted_label==5);
h5 = plot(dd(pos,1),dd(pos,2),'s','color',dcolor,'MarkerSize',10,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',dcolor);
hold on 
uistack(h1, 'bottom');
uistack(h2, 'bottom');
uistack(h3, 'bottom');
uistack(h4, 'bottom');
uistack(h5, 'bottom');

hold on
plot(PCAX(1:1000,1),PCAX(1:1000,2),'. r');
hold on
plot(PCAX(1001:2000,1),PCAX(1001:2000,2),'. g');
hold on
plot(PCAX(2001:3000,1),PCAX(2001:3000,2),'. b');
hold on
plot(PCAX(3001:4000,1),PCAX(3001:4000,2),'. m');
hold on
plot(PCAX(4001:5000,1),PCAX(4001:5000,2),'. y');
hold on
plot(sv(:,1),sv(:,2),'ko', 'MarkerSize', 5);
hold off

%{
figure
index1 =find(predict_labeltrain==1); 
data1 = (PCAX(index1,:))'; 
plot(data1(1,:),data1(2,:),'or');
hold on 
index2 =find(predict_labeltrain==2); 
data2 = (PCAX(index2,:))';
plot(data2(1,:),data2(2,:),'*'); 
hold on 
indexw = find(predict_labeltrain~=(label));
dataw = (PCAX(indexw,:))';
plot(dataw(1,:),dataw(2,:),'+g'); 
%}

