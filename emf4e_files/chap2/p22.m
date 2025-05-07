load p22_mag.dat
mmf=p22_mag(:,1);
phi=p22_mag(:,2)/1000.;
clear p22_mag;
plot(mmf,phi,'LineWidth',2.0);
grid on;
title('\bfMagnetization curve for 120/240-V transformer');
xlabel ('\bfMMF, A-turns');
ylabel ('\bfFlux, Wb');