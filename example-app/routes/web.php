<?php

use App\Http\Controllers\Api\CandidateResourceController;
use App\Http\Controllers\ApiConsume;
use App\Http\Controllers\CandidateController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

//Route::get('/',[ApiConsume::class,'test']);
Route::get('/',function(){
    return view('welcome');
});

Route::get('apiconsume',[ApiConsume::class,'test']);

Route::get('/candidates',[CandidateController::class,'index']);


Route::get('jsontocsv',[CandidateResourceController::class,'GeraPython']);
