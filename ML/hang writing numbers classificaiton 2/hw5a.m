xtrain= csvread('X_train.csv');%讀取檔案
ttrain = csvread('T_train.csv');
xtest = csvread('X_test.csv');
ttest = csvread('T_test.csv');
%lda
%{
Train=cell(1,length(ttrain));
for i=1:1000
    Train(i)={'1'};
    Train(i+1000)={'2'};
    Train(i+2000)={'3'};
    Train(i+3000)={'4'};
    Train(i+4000)={'5'};
end    
xtrain=xtrain;

mLDA=LDA(xtrain,Train);
mLDA.Compute();
transformedTrainSamples = mLDA.Transform(xtrain, 1);
transformedTestSamples = mLDA.Transform(xtest, 1);
calculatedClases = knnclassify(transformedTestSamples, transformedTrainSamples, Train);
%}



[eigenVectors,score,eigenValues,tsquare]= princomp(xtrain);
transMatrix = eigenVectors(:,1:2);  %取前兩大
%testing data 降為
Asum=sum(xtrain)/4999; 
AT=transpose(xtest);
B=zeros([784 2500]);         
for i=1:784
B(i,:)=AT(i,:)-Asum(i);
end
xtestpca=transpose(B)*transMatrix;
%training data 降為
RT=transpose(xtrain);
R=zeros([784 5000]); 
for i=1:784
R(i,:)=RT(i,:)-Asum(i);
end
xtrainpca=transpose(R)*transMatrix;

b = TreeBagger(100,xtrainpca,ttrain,'InBagFraction',1,'OOBPred','on','Method','classification','minleaf',100)
%b = TreeBagger(100,xtrain,ttrain,'InBagFraction',1,'OOBPred','on','Method','classification','minleaf',100)
view(b.Trees{1},'Mode','graph')
%{
figure;
oobErrorBaggedEnsemble = oobError(b);
plot(oobErrorBaggedEnsemble)
xlabel 'Number of grown trees';
ylabel 'Out-of-bag classification error';
%}
%??
[K] = predict(b, xtestpca);   
%[K] = predict(b, xtest);
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
%繪decision region

figure(1)

PCAX=xtrainpca;
[xi,yi] = meshgrid([min(xtrainpca(:,1)):0.1:max(xtrainpca(:,1))],[min(xtrainpca(:,2)):0.1:max(xtrainpca(:,2))]);
dd = [xi(:),yi(:)];
[A] = predict(b,dd); 
predicted_label=str2num(char(A));

redcolor = [1 0.8 0.8];
bluecolor = [0.8 0.8 1];
greencolor = [0.8 1 0.8];
ccolor = [0.5 1 0.3];
dcolor = [0.2 0.6 0.3];
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
plot(PCAX(1:1000,1),PCAX(1:1000,2),'. r');
hold on
plot(PCAX(1001:2000,1),PCAX(1001:2000,2),'. g');
hold on
plot(PCAX(2001:3000,1),PCAX(2001:3000,2),'. b');
hold on
plot(PCAX(3001:4000,1),PCAX(3001:4000,2),'. m');
hold on
plot(PCAX(4001:5000,1),PCAX(4001:5000,2),'. y');
axis([min(xtrainpca(:,1)),max(xtrainpca(:,1)),min(xtrainpca(:,2)),max(xtrainpca(:,2))])
hold on

