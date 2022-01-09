from flask import Flask, render_template, url_for, request, send_file, flash
from forms import MainForm
import faceswap as FaceSwap
import os

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
		try:
			mf.save(f"{os.getcwd()}\FaceSwapApp\static\input\{mf.filename}")
			sf.save(f"{os.getcwd()}\FaceSwapApp\static\input\{sf.filename}")
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
			FaceSwap.swap(f"{os.getcwd()}\FaceSwapApp\static\input\{mf.filename}",
					f"{os.getcwd()}\FaceSwapApp\static\input\{sf.filename}")
		except FaceSwap.NoFaceException:
			print("A Face could not be detected!")
			flash("A Face could not be detected! Only human faces are detected", "danger")
			exceptionOccured = True
			return render_template('main.html', form=form)
		except FaceSwap.MoreThanOneFaceException:
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
		ofacepic = url_for('static', filename=f"output/{outpath}")
		return render_template('main.html', form=form, mfp=mfacepic, sfp=sfacepic, ofp=ofacepic, fn=outpath.split(".")[0])
	return render_template('main.html', form=form)

@app.route("/download/<fn>")
def download(fn):
	print("Download request recieved")
	return send_file(f"{os.getcwd()}\FaceSwapApp\static\output\{fn}.jpg", as_attachment=True, mimetype="image/jpeg")


if(__name__ == '__main__'):
	#Runs on localhost:8080
	app.run(debug=True, host='localhost', port=8080)
