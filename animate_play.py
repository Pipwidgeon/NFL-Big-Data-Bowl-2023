# Script by Nick Wan, downloaded 22/11/07
# source: https://www.kaggle.com/code/nickwan/animated-gif-for-plays-python

import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 

# for mpl animation
import matplotlib.animation as animation
from matplotlib import rc
rc('animation', html='html5')

def get_play_by_frame(fid, ax, los, one_play):
  """
  take one frame from one play, plot a scatter plot image  

  inputs:
    fid: frame ID  
    ax: current matplotlib ax  
    los: line of scrimmage (for aesthetics)  
    one_play: pandas dataframe for one play  

  output:
    seaborn axis level scatter plot  
  """
  # clear current axis (or else you'll have a tracer effect)
  ax.cla()

  # get game and play IDs
  gid = one_play['gameId'].unique()[0]
  pid = one_play['playId'].unique()[0]

  # isolates a given frame within one play
  one_frame = one_play.loc[one_play['frameId']==fid]

  # create a scatter plot, hard coded dot size to 100 
  fig1 = sns.scatterplot(x='x',y='y',data=one_frame, 
                         hue='team', ax=ax, s=100)
  
  # plots line of scrimmage 
  fig1.axvline(los, c='k', ls=':')

  # plots a simple end zone 
  fig1.axvline(0, c='k', ls='-')
  fig1.axvline(100, c='k', ls='-')

  # game and play IDs as the title
  fig1.set_title(f"game {gid} play {pid}")

  # takes out the legend (if you leave this, you'll get an annoying legend)
  fig1.legend([]).set_visible(False)

  # takes out the left, top, and right borders on the graph 
  sns.despine(left=True)

  # no y axis label
  fig1.set_ylabel('')

  # no y axis tick marks
  fig1.set_yticks([])

  # set the x and y graph limits to the entire field (from kaggle BDB page)
  fig1.set_xlim(-10,110)    
  fig1.set_ylim(0,54) 

def animate_play(one_play):    
  """
  animate a given NFL play from the BDB  

  inputs: 
    one_play: one play from the BDB data. you will want to 
      filter your dataset using gameId and playId.

  output: 
    animated gif, saved to your current working directory 

  """
  # get game and play IDs
  gid = one_play['gameId'].unique()[0]
  pid = one_play['playId'].unique()[0]

  # get line of scrimmage info from the football X location from the  first frame of data 
  los = one_play.loc[(one_play['frameId']==1) & (one_play['team']=='football'), 'x'].values[0]

  # set figure size; this is hard coded but seemed to work well  
  fig = plt.figure(figsize=(14.4, 6.4))

  # get current axis of the figure
  ax = fig.gca()

  # matplotlib animate function
  # relies on get_play_by_frame()  
  # `interval = 100` is something like frames per second i think 
  # repeat=True is to have the animation continuously repeat  
  ani = animation.FuncAnimation(fig, get_play_by_frame, 
                                frames=one_play['frameId'].unique().shape[0],
                                interval=100, repeat=True, 
                                fargs=(ax,los,one_play,))
  
  # close the matplotlib figure when done (if you're batch processing gifs, this allows you to end one gif and begin another gif of a play)
  #plt.close()

  # save the matplotlib animation as a gif
  # requires imagemagick or some sort of gif renderer
  # this works in google colab if you apt install imagemagick
  #ani.save(f'{gid}_{pid}.gif', writer='imagemagick', fps=10)
  return ani    