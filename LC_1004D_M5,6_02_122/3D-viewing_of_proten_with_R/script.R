#install.packages("bio3d")
#install.packages("rgl")
library(bio3d)
library(rgl)

# Load example PDB structure
pdb <- read.pdb("1CRN") 

ca.inds <- atom.select(pdb, elety = "CA")
coords <- pdb$xyz[ca.inds$xyz]
n_frames <- 30

# Create fake trajectory: random wiggles
set.seed(42)
fake_trj <- matrix(rep(coords, n_frames), nrow = n_frames, byrow = TRUE)
noise <- matrix(rnorm(length(fake_trj), mean = 0, sd = 0.5), nrow = n_frames)
fake_trj <- fake_trj + noise
for (i in 1:n_frames) {
  frame <- matrix(fake_trj[i, ], ncol = 3, byrow = TRUE)
  plot3d(frame, type = "s", col = "purple", size = 0.6,
         xlab = "X", ylab = "Y", zlab = "Z", main = paste("Frame", i))
  Sys.sleep(0.1)
}

rmsd_values <- vector()

for (i in 1:n_frames) {
  frame <- fake_trj[i, ]
  rmsd <- rmsd(pdb$xyz[ca.inds$xyz], frame)
  rmsd_values[i] <- rmsd
}

plot(1:n_frames, rmsd_values, type = "b", col = "darkgreen",
     xlab = "Frame", ylab = "RMSD (Å)", main = "RMSD Across Frames")

for (i in 1:n_frames) {
  frame <- matrix(fake_trj[i, ], ncol = 3, byrow = TRUE)
  rmsd <- round(rmsd_values[i], 2)
  plot3d(frame, type = "s", col = "purple", size = 0.6,
         xlab = "X", ylab = "Y", zlab = "Z",
         main = paste("Frame", i, "- RMSD:", rmsd, "Å"))
  Sys.sleep(0.2)
}

rmsf_values <- rmsf(fake_trj)
plot(rmsf_values, type = "h", col = "steelblue", xlab = "Residue", ylab = "RMSF (Å)")

write.csv(data.frame(Frame = 1:n_frames, RMSD = rmsd_values), "trajectory_metrics.csv")

write.csv(data.frame(Frame = 1:n_frames, RMSD = rmsd_values), "rmsd_data.csv")
