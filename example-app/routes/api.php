<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\CandidateResourceController;
use App\Http\Controllers\Api\Candidates;
use App\Http\Controllers\Api\CandidatosController;
use App\Http\Controllers\Api\Testing;
use App\Http\Controllers\Api\TopVotos;
use App\Http\Controllers\Api\VotesNeighborhoods as ApiVotesNeighborhoods;
use App\Http\Resources\CandidateResource;
use App\Models\Candidate;
use App\Models\User;
use App\Models\VotesNeighborhoods;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Route;




/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

// CPF   29226613850

// Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
//     return $request->user();
// });



// Route::apiResource('candidates',Candidates::class)->only('index','show');

// Route::apiResource('candidates.votesneighborhood',ApiVotesNeighborhoods::class)->only('index','show');



//Route::apiResource('candidatesRe',CandidateResourceController::class)->only('show','index');

Route::get('candidatosMaisVotados/{qt?}',[TopVotos::class,'CidadeMaisVotada']);//->only('show','index');


//Route::get('candidatosMost/{qt?}','App\Http\Controllers\Api\CandidateResourceController@dados');//->only('show','index');

Route::post('login',[AuthController::class,'login']);
Route::post('/password/email',[AuthController::class,'sendPasswordResetLinkEmail']);
Route::post('/password/reset',[AuthController::class,'resetPassword']);

Route::group(['middleware' => ['auth:sanctum']],function(){

    Route::apiResource('candidatos',CandidateResourceController::class)->only('show','index');
});
//Route::apiResource('candidatos',CandidateResourceController::class)->only('show','index');

Route::get('creat',function(){

    User::create([
        'name' => 'allan',
        'email' => 'allan@gmail.com',
        'password' => Hash::make('123'),
        'is_admin' => true,
    ]);
});

// no AuthServiceProvider Precisa Criar Reset Passowrd;

// ele usa uma tabela chamada aulas e controler AulasController
// ele usa tabela chamado aulas


// Store e Product -mf ele criou
// tabela stores e tabela products

// class Store tem 1 funsao chamada products hasMany(Product::class) //store_id

// course = Course::with('modules.lessons')->first();



/*
stores é tabela mae O MODEL tme metore store()belogsto(Store:class) sem id

products tem store_id possui metodo products()hasMany(Product::class) com sore_id
*/
