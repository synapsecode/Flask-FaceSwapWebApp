from flask import Flask, render_template, url_for, request, send_file, flash
from faceswap import FaceSwap, NoFaceException, MoreThanOneFaceException
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os

class MainForm(FlaskForm):
	main_file = FileField()
	second_file = FileField()
	submit = SubmitField('Merge Faces')

app = Flask(__name__)
app.secret_key = "NF484j33hSDDJFH9s83nb"

@app.route("/", methods=['GET', 'POST'])
def homepage():
	form = MainForm()
	if(form.is_submitted()):
		exceptionOccured=False
		print("Submitted")
		#save input files
		mf = request.files['main_file']
		sf = request.files['second_file']
		img1 = os.path.join(os.getcwd(), 'static', 'input', mf.filename)
		img2 = os.path.join(os.getcwd(), 'static', 'input', sf.filename)
		try:
			mf.save(img1)
			sf.save(img2)
		except FileNotFoundError:
			print("Input file not supplied")
			flash("Please Reload the images and submit", "danger")
			return render_template('main.html', form=form)
		except Exception as e:
			flash("An Unknown Error has occured.", "danger")
			print(e)
			return render_template('main.html', form=form)
		print("Saved Input Files")

		#Merge Faces
		try:
			FaceSwap(img1, img2)
		except NoFaceException:
			print("A Face could not be detected!")
			flash("A Face could not be detected! Only human faces are detected", "danger")
			exceptionOccured = True
			return render_template('main.html', form=form)
		except MoreThanOneFaceException:
			print("There seems to be more than one face in the image")
			flash("There seems to be more than one face in the images. There must be only one well defined face", "danger")
			exceptionOccured = True
			return render_template('main.html', form=form)
		except Exception as e:
			print(e)
			flash("An Unknown Error has occured", "danger")
			return render_template('main.html', form=form)
		print("Done Swapping")

		#Give Back Image
		mfacepic = url_for('static', filename=f"input/{mf.filename}")
		sfacepic = url_for('static', filename=f"input/{sf.filename}")
		outpath = mf.filename.split(".")[0] + "-" + sf.filename.split(".")[0] + ".jpg"
		print(f"OUTPATH: {outpath}")
		ofacepic = url_for('static', filename=f"output/{outpath}")
		return render_template('main.html', form=form, mfp=mfacepic, sfp=sfacepic, ofp=ofacepic, fn=outpath.split(".")[0])
	return render_template('main.html', form=form)


@app.route("/download/<fn>")
def download(fn):
	print("Download request recieved")
	path = os.path.join(os.getcwd(), 'static', 'output', f'{fn}.jpg')
	return send_file(path, as_attachment=True, mimetype="image/jpeg")


if(__name__ == '__main__'):
	#Runs on localhost:8080
	app.run(debug=True, host='localhost', port=8080)
