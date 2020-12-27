library(ggplot2)
library(dplyr)
library(magrittr)

library(gganimate)

a <- seq(from = 10, to = 20, length.out = 100)




alldata <- do.call(bind_rows, lapply(X = seq_along(a), FUN = function(i) {
  tibble(xstart = c(-1, -1, -1)*4,
         xend = c(1, 1, 1) * 4,
         y = c(0.95, 1, 1.05) * a[i],
         type = c("Threshold", "SMA", "Threshold")) %>% bind_cols(frame = i)
}))


p <- alldata %>% ggplot(aes(x = xstart, y = y, xend = xend, yend = y)) + 
  geom_segment(aes(color = type)) + 
  lims(x = c(-4, 4), y = c(9, 21)) + 
  labs(x = "Date", y = "Price",
       title = " ", color = "") + 
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5),
        panel.border = element_blank())
p

p + transition_manual(frame) + labs(subtitle = "a: {frame}") 


anim_save(filename = "test2.gif")



