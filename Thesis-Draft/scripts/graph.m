%% Initialize variables.
filename = '/Users/Sandipan/Desktop/Test/mems.csv';
delimiter = ',';
startRow = 6;

%% Format string for each line of text:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%f%f%q%f%[^\n\r]';
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(fileID);

%% Allocate imported array to column variable names
K=100;
w_RR = dataArray{:, 1};
w_slab = dataArray{:, 2};
%Slab width actual sizie scaling
w_slab = w_slab + 0.15;
w_RR(:) = round(w_RR(:)*K);
w_slab(:) = round(w_slab(:)*K);

lambda = abs(str2double(dataArray{:, 3}));
% Ratio of the polarization
rp = abs(real(log10(dataArray{:, 4})));
k = lambda>=1;
sums = accumarray( { w_RR(k), w_slab(k)}, rp(k),[],[],[],true );
[i,j,k] = find(sums);

%% Draw area chart
figure
hold on
matrix = [i/K j/K k];
tri = delaunay(matrix(:,1),matrix(:,2));
trisurf(tri,matrix(:,1),matrix(:,2),matrix(:,3))
shading faceted
grid on
hold off

%%Draw 5 max on graph
hold on
N = 5;
[sortedX, sortedInds] = sort(k(:),'ascend');
topN = sortedInds(1:N);
[m] = ind2sub(size(k), topN);

h = scatter3(i(m)/K,j(m)/K,k(m),'filled', 'MarkerFaceColor','red');
h.SizeData = 100;

text(i(m)/K,j(m)/K,k(m),strcat('(',num2str(i(m)/K),',',num2str(j(m)/K),')'),'HorizontalAlignment','left', 'Color', 'red', 'FontSize', 12)
hold off

%% Labels
xlabel('Rib width in \mum', 'FontSize',18,'FontWeight','bold','Color','black')
ylabel('Base width in \mum', 'FontSize',18,'FontWeight','bold','Color','black')

zlabel_eq = '$$\sum_{mode}{abs\left(log \frac{E_{x_{mode}}}{E_{y_{mode}}}\right)}$$';
zlabel(strcat('Log ratio of E-field = ', zlabel_eq), 'FontSize',22,'FontWeight','bold','Color','black','Interpreter','latex')

%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;