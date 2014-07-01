#ifndef VIDEO_H
#define VIDEO_H

#include <QtWidgets/QMainWindow>
#include <qprocess.h>
#include <qthread.h>
#include "ui_video.h"

class Ticker : public QThread {
	Q_OBJECT

	public:
		int running;
		void run();

	signals:
		void tick();
};

class Loader : public QThread {
	Q_OBJECT

	public:
		Loader(QWidget * parent, QString filename);
		QString filename, tmp;
		int finished = 1;
		__int64 size, pos;
		void run();
		void quit();

	signals:
		void done(const QString &result);
};

class video : public QMainWindow
{
	Q_OBJECT

	public:
		video(QWidget *parent = 0);
		void load_file(QString filename);
		void load_file();

	public slots:
		void play();
		void tick();
		void set_volume(int to);
		void audio_source(int index);
		void menu_select(QAction*);

	private:
		Ui::MainWindow ui;
		int audio_from = 0;
		void add_video(QString path);
		QSlider * volume;
		QProgressBar * load_meter;
		QComboBox * audio;
		QGridLayout * grid;
		QString filename;
		Loader * loader;
		Ticker * ticker;
};

#endif // VIDEO_H
