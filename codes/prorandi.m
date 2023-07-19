% a1, a2, a3 - the border of the two ranges
% pro - the probability of the first range(%), the other is 1-pro
function aa = prorandi(a1, a2, a3, pro)
index_1 = randi([1, 100]);
if index_1 <= pro
    index_2 = 1;
else
    index_2 = 2;
end

if index_2 == 1
    aa = randi([a1, a2]);
else
    aa = randi([a2, a3]);
end
end